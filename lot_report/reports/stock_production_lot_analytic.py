# -*- coding: utf-8 -*-
from odoo import models, fields, tools, api


class stocklotupdateanalytic(models.Model):
    _name = 'stock.production.lot.update.analytic'

    @api.multi
    def update_qty(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for line in self.env['stock.production.lot'].search([]):
            quants = line.quant_ids.filtered(lambda q: q.location_id.usage in ['internal', 'transit'])
            line.product_qty_c = sum(quants.mapped('quantity'))

        return {'type': 'ir.actions.act_window_close'}


class stock_production_lot_analytic(models.Model):
    _name = 'stock.production.lot.analytic'

    _auto = False
    _rec_name = 'name'
    _order = 'id desc'
    id = fields.Integer('ID')

    name = fields.Char('Name')
    barcode = fields.Char('Barcode')
    product_id = fields.Many2one(
        'product.product', string='Product Variant', readonly=1)

    purchase_order_id = fields.Many2one('purchase.order', string='PO')
    related_vendor_id = fields.Many2one('res.partner', string='Related Vendor')
    partner_id = fields.Many2one('res.partner', string='Vendor')
    company_id = fields.Many2one(
        'res.company', string='Company', readonly=1)
    product_qty_c = fields.Float('Rest Quantity')
    product_qty_po = fields.Float('Tolal Qty purchase')
    product_cost_po = fields.Float('product cost purchase')
    product_qty_sale = fields.Float('Quantity Sale')
    product_cost_sale = fields.Float('Total Sale Cost')

    def _lot_select(self):
        select = """SELECT min(pol.id) as id,
            pol.name as name,
            pol.barcode as barcode,
            pol.product_id as product_id,
            pol.purchase_order_id as purchase_order_id,
            pol.related_vendor_id as related_vendor_id,
            pol.partner_id as partner_id,
            pol.company_id as company_id,
            pol.product_qty_c as product_qty_c,

            po.product_qty AS product_qty_po,
            po.price_unit AS product_cost_po,
            sum(po.product_qty - pol.product_qty_c) as product_qty_sale,
            (sum(po.product_qty - pol.product_qty_c) * po.price_unit)  as product_cost_sale

            FROM stock_production_lot pol
            LEFT JOIN purchase_order_line po ON po.order_id = pol.purchase_order_id

            WHERE po.lot_name=pol.barcode and  po.lst_price=pol.lst_price
            GROUP BY pol.name, pol.barcode, pol.product_id,pol.purchase_order_id, pol.related_vendor_id,
            pol.partner_id, pol.company_id,pol.product_qty_c,po.product_qty,po.price_unit
        """
        return select

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("CREATE OR REPLACE VIEW %s AS (%s)" % (
            self._table, self._lot_select()))
