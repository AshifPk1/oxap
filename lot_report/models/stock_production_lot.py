# -*- coding: utf-8 -*-
from odoo import models, fields, tools, api


class stocklotupdate(models.Model):
    _name = 'stock.production.lot.update'

    @api.multi
    def update_qty(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for line in self.env['stock.production.lot'].search([]):
            quants = line.quant_ids.filtered(lambda q: q.location_id.usage in ['internal', 'transit'])
            line.product_qty_c = sum(quants.mapped('quantity'))

        return {'type': 'ir.actions.act_window_close'}


class stocklot(models.Model):
    _inherit = 'stock.production.lot'

    product_qty_c = fields.Float('Quantity')
