from datetime import date

from odoo import models, fields, api
from odoo.tools import float_compare, UserError


class purchase_order(models.Model):
    _inherit = "purchase.order"

    date_today = fields.Date('Date', default=date.today(), readonly=True, )
    is_frame_purchase = fields.Boolean(default=False)
    is_lense_purchase = fields.Boolean(default=False)
    is_surgicallense_purchase = fields.Boolean(default=False)
    is_pharmacy_purchase = fields.Boolean(default=False)

    @api.multi
    def button_confirm_all(self):
        for line in self.order_line:
            if line.product_id.type == 'product':
                if line.product_id.tracking =='lot':
                    if line.prod_lot_id:
                        for move_line in line.move_ids:
                            if len(move_line.move_line_ids) > 1 and move_line.move_line_ids[
                                0].lot_id.id != line.prod_lot_id.id:
                                move_line.move_line_ids.unlink()
                                move_line_id = self.env['stock.move.line'].create(move_line._prepare_move_line_vals())
                                move_line_id.lot_id = line.prod_lot_id.id
                                move_line_id.qty_done = line.product_qty
                            else:
                                for each_l in move_line.move_line_ids:
                                    each_l.lot_id = line.prod_lot_id.id
                                    each_l.qty_done = line.product_qty
                                    each_l.expiry_date = line.expiry_date
                                    each_l.sale_price = line.sale_price
                    else:
                        raise UserError('Add Lot To the Product')
                else:
                    for each_l in line.move_ids.move_line_ids:
                        each_l.qty_done = line.product_qty
        self.picking_ids.button_validate()
        new_invoice = self.env['account.invoice'].create({
                'type': 'in_invoice',
                'purchase_id': self.id,
                'partner_id': self.partner_id.id,
                'account_id': self.partner_id.property_account_payable_id.id,
            })
        new_invoice.purchase_order_change()




class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    prod_lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number',
                                  domain="[('product_id','=', product_id)]")
    expiry_date = fields.Datetime('Expiry Date',store=True)

    sale_price = fields.Float('Sale Price',store=True)

    is_lot_product = fields.Boolean('Is Lot', default=True)

    @api.onchange('prod_lot_id')
    def _onchange_prod_lot_id(self):
        self.expiry_date =False
        self.sale_price = False
        if self.prod_lot_id:
            if self.prod_lot_id.exp_date_test:
                self.expiry_date = self.prod_lot_id.exp_date_test
            if self.prod_lot_id.sale_price:
                self.sale_price = self.prod_lot_id.sale_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.is_lot_product = True
        self.expiry_date = False
        self.sale_price = False
        self.prod_lot_id = False
        if self.product_id:
            if self.product_id.type == 'product':
                if self.product_id.tracking != 'lot':
                    self.is_lot_product = False

    @api.onchange('sale_price')
    def _onchange_sale_price(self):
        if self.sale_price:
            if self.product_id:
                if self.product_id.type == 'product':
                    if self.product_id.tracking != 'lot':
                        product = self.env['product.product'].search([('id', '=', self.product_id.id)])
                        product.write({
                            'lst_price':self.sale_price
                        })








