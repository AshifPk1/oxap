from datetime import date
from datetime import datetime
from odoo import models, fields, api


class StockproductionLot(models.Model):
    _inherit = 'stock.production.lot'
    _order = 'life_date'
    expiry_date = fields.Date(string='Expiry Date', required=False, store=True)

    expiry_status = fields.Selection([
        ('Active', 'Active'),
        ('Expired', 'Expired')], compute='compute_expiry_status', string='Expiry Status', default='Active', store=True)
    sale_price = fields.Float('Sale Price', store=True)
    exp_date_test = fields.Datetime('Exp Date Test', store=True)
    qty_available = fields.Float(string='Stock', compute='_qty_available')

    @api.multi
    @api.depends('exp_date_test')
    def compute_expiry_status(self):
        for record in self:
            if record.exp_date_test:
                to_date = datetime.strptime(record.exp_date_test, "%Y-%m-%d %H:%M:%S").date()
                if to_date < date.today():
                    record.expiry_status = 'Expired'
                else:
                    record.expiry_status = 'Active'

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.exp_date_test:
                exp_date_test = datetime.strptime(record.exp_date_test, "%Y-%m-%d %H:%M:%S").date()
                name = "%s / %s /%s" % (record.name, str(exp_date_test), record.expiry_status)
                result.append((record.id, name))
            else:
                for record in self:
                    name = "%s / %s" % (record.name, "No Expiry Date")
                    result.append((record.id, name))
        return result

    @api.one
    def _qty_available(self):
        for rec in self:
            quantity = 0.0
            reserved_quantity = 0.0
            quants = rec.quant_ids.filtered(lambda q: q.location_id.usage in ['internal'])
            quantity = sum(quants.mapped('quantity'))
            reserved_quantity = sum(quants.mapped('reserved_quantity'))
            rec.qty_available = quantity - reserved_quantity
