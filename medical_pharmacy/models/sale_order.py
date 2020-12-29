from odoo import api, models, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    doctor_id = fields.Many2one('medical.practitioner', string='Doctor', readonly=True)

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            if line.lot_number_id:
                for move_line in line.move_ids:
                    if len(move_line.move_line_ids) > 1 and move_line.move_line_ids[
                        0].lot_id.id != line.lot_number_id.id:
                        move_line.move_line_ids.unlink()
                        move_line_id = self.env['stock.move.line'].create(move_line._prepare_move_line_vals())
                        move_line_id.lot_id = line.lot_number_id.id
                        move_line_id.qty_done = line.product_uom_qty

                    else:
                        for each_l in move_line.move_line_ids:
                            each_l.lot_id = line.lot_number_id.id
                            each_l.qty_done = line.product_uom_qty

        return res
