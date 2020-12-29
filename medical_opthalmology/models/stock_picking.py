from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.sale_id:
            self.sale_id.delivery_status = 'delivered'
        return res
