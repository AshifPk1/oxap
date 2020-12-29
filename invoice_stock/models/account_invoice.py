# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    barcode = fields.Char('Lot qr / Barcode')

    lot_id = fields.Many2one('stock.production.lot', string='lot', )

    @api.onchange('barcode')
    def _onchange_barcode_scan(self):
        lot = self.env['stock.production.lot']
        if self.barcode:
            loto = lot.search([('barcode', '=', self.barcode), ('company_id', '=', self.env.user.company_id.id)])
            if loto:
                for lo in loto:
                    self.product_id = lo.product_id.id
                    self.lot_id = lo.id
                    self.qty = lo.product_qty

                    self.quantity = lo.product_qty
            else:
                product_rec = self.env['product.product']

                product = product_rec.search([('barcode', '=', self.barcode)])
                if product:
                    self.product_id = product.id


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _default_picking_type(self):
        inv_type = self._context.get('type', 'out_invoice')
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        picking_type_obj = self.env['stock.picking.type']
        if inv_type == 'out_refund':
            types = picking_type_obj.search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)],
                                            limit=1)
            if not types:
                types = picking_type_obj.search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
            return types[:1]
        elif inv_type == 'in_refund':
            types = picking_type_obj.search([('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)],
                                            limit=1)
            if not types:
                types = picking_type_obj.search([('code', '=', 'outgoing'), ('warehouse_id', '=', False)])
            return types[:1]
        else:
            return False

    picking_ids = fields.One2many('stock.picking', 'invoice_id', string='Pickings')
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', required=False,
                                      default=_default_picking_type)
    auto_validate_delivey = fields.Boolean(default=True, string='Auto Validate Delivery', copy=False,
                                           track_visibility='always')

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()

        for each in self:
            if each.type in ['in_refund', 'out_refund'] and each.picking_type_id:
                Picking = self.env['stock.picking']
                warehouse_obj = self.env['stock.warehouse']
                customerloc, supplierloc = warehouse_obj._get_partner_locations()
                if each.type == 'out_refund':
                    if not each.picking_type_id.default_location_src_id:
                        location = customerloc.id
                    else:
                        location = each.picking_type_id.default_location_src_id.id

                else:
                    if not each.picking_type_id.default_location_dest_id:
                        location = supplierloc.id
                    else:
                        location = each.picking_type_id.default_location_src_id.id

                picking = Picking.create(each._get_new_picking_values(location))
                if picking:
                    for each_line in each.invoice_line_ids:
                        if each.type == 'out_refund':
                            destination = self.picking_type_id.default_location_dest_id.id or False
                            source = location
                        else:
                            destination = location
                            source = self.picking_type_id.default_location_src_id.id or False

                        move_val = {
                            'name': each_line.product_id.name,
                            'product_id': each_line.product_id.id,
                            'product_uom_qty': each_line.quantity,
                            'product_uom': each_line.uom_id.id or False,
                            'location_id': source,
                            'location_dest_id': destination,
                            'invoice_line_id': each_line.id,
                            'picking_id': picking.id}
                        move_line = self.env['stock.move'].create(move_val)

                if res and self.auto_validate_delivey:
                    for pick in self.picking_ids:
                        pick.action_assign()
                        lines_to_check = pick.move_lines
                        for line in lines_to_check:
                            line.qty_done = line.product_uom_qty
                            line.quantity_done = line.product_uom_qty
                            if line.invoice_line_id and line.invoice_line_id.lot_id:
                                for each_l in line.move_line_ids:
                                    each_l.lot_id = line.invoice_line_id.lot_id.id
                                    each_l.qty_done = line.product_uom_qty
                        pick.force_assign()
                        pick.action_done()
            else:
                if res and self.auto_validate_delivey:
                    for pick in self.picking_ids:

                        lines_to_check = pick.move_lines
                        for line in lines_to_check:
                            line.qty_done = line.product_uom_qty
                            line.quantity_done = line.product_uom_qty

                        pick.action_assign()
                        pick.force_assign()
                        pick.action_done()
        return res

    def _get_new_picking_values(self, location):
        """ Prepares a new picking for this move as it could not be assigned to
        another picking. This method is designed to be inherited. """

        if self.type == 'out_refund':
            destination = self.picking_type_id.default_location_dest_id.id or False
            source = location
        else:
            destination = location
            source = self.picking_type_id.default_location_src_id.id or False
        print(destination, source)
        return {
            'invoice_id': self.id,
            'scheduled_date': self.date_invoice,
            'origin': self.number,
            'company_id': self.company_id.id,
            'move_type': 'direct',
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_id.id,
            'location_id': source,
            'location_dest_id': destination,
        }

    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(order.picking_ids)

    @api.multi
    def action_view_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = pickings.id
        return action
