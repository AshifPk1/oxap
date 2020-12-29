from odoo import api, models, fields
from odoo.exceptions import ValidationError


class PharmacyPrescription(models.Model):
    _name = 'pharmacy.prescription'

    patient_visit_id = fields.Many2one('medical.pharmacy')

    product_id = fields.Many2one('product.product', string='Product', domain=[('is_pharmacy', '=', True)])
    quantity = fields.Float('Qty', required=True, default=1)
    price_unit = fields.Float('Price Unit')
    sub_total = fields.Float('Sub Total', compute='compute_sub_total')
    code = fields.Char('Code', compute='compute_pharmacy_product_id_code')
    lot_number_id = fields.Many2one('stock.production.lot', string='Batch',
                                    domain="[('product_id', '=', product_id),('expiry_status','=','Active')]")
    qty_available = fields.Float('Stock', readonly=True, store=True)

    tax_ids = fields.Many2many('account.tax', string='Tax')

    price_tax = fields.Float(compute='_compute_amount', string='Taxes', readonly=True, store=True)
    discount = fields.Float('Discount', readonly=True)
    price_total = fields.Float(compute='_compute_amount', string='Total', readonly=True, store=True)

    @api.depends('product_id', 'quantity', 'price_unit')
    def compute_sub_total(self):
        for record in self:
            record.sub_total = record.price_unit * record.quantity

    @api.depends('product_id')
    def compute_pharmacy_product_id_code(self):
        for rec in self:
            rec.code = rec.product_id.l10n_in_hsn_code

    @api.onchange('product_id')
    def _onchange_product_ids(self):
        prodcut_templ = self.env['product.template'].search([('id', '=', self.product_id.product_tmpl_id.id)])
        self.price_unit = self.product_id.list_price
        record = self.env['stock.production.lot'].search(
            [('product_id', '=', self.product_id.id), ('expiry_status', '=', 'Active'), ('product_qty', '>', 0)])
        if record:
            ids = []
            for item in record:
                if item.product_qty > 0:
                    ids.append(item.id)
            return {'domain': {'lot_number_id': [('id', 'in', ids)]}}
        else:
            return {'domain': {'lot_number_id': [('id', 'in', [])]}}

    @api.onchange('lot_number_id')
    def _onchange_lot_number_id(self):
        self.price_unit = self.lot_number_id.sale_price
        self.qty_available = self.lot_number_id.qty_available

    @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', )
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.patient_visit_id.currency_id, line.quantity,
                                             product=line.product_id, partner=False)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
            })

    @api.onchange('quantity')
    def onchange_quantity(self):
        if self.quantity:
            if self.lot_number_id:
                if self.quantity > self.qty_available:
                    raise ValidationError('Selling qty should not be greater than available qty')
