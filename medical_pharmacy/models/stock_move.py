# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    expiry_date = fields.Date('Expiry Date', store=True)
    sale_price = fields.Float('Sale Price', store=True)

    @api.onchange('lot_id')
    def on_change_lot_id(self):
        if self.lot_id:
            if self.lot_id.sale_price or self.lot_id.exp_date_test:
                self.expiry_date = self.lot_id.exp_date_test
                self.sale_price = self.lot_id.sale_price

    def _action_done(self):
        for ml in self:
            if ml.lot_id and ml.sale_price and ml.expiry_date:
                ml.lot_id.update({
                    'sale_price': ml.sale_price,
                    'exp_date_test': ml.expiry_date,
                })
        res = super(StockMoveLine, self)._action_done()
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    sale_price = fields.Char('Sale Price', compute='compute_lot_sale_price')
    lot_id = fields.Char('Lot', compute='compute_lot_sale_price')

    @api.depends('move_line_ids.lot_id', 'move_line_ids.sale_price')
    def compute_lot_sale_price(self):
        for rec in self:
            for line in rec.move_line_ids:
                if line.lot_id and line.sale_price:
                    if rec.lot_id == False:
                        rec.lot_id = ''
                        rec.sale_price = ''
                        rec.lot_id += (str(line.lot_id.name) + '/')
                        rec.sale_price += (str(line.sale_price) + '/')
                    else:
                        rec.lot_id += str(line.lot_id.name + '/')
                        rec.sale_price += (str(line.sale_price) + '/')
