from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    patient_visit_id = fields.Many2one('medical.opthalmology', 'Patient Visit ID')
    identification_code = fields.Char('File Number', readonly=True)
    state = fields.Selection(selection_add=[('invoiced', 'Invoiced'), ('paid', 'Paid')])
    delivery_status = fields.Selection([
        ('not_delivered', 'Not Delivered'),
        ('delivered', 'Delivered'),
    ], default='not_delivered')

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create(grouped=False, final=False)
        self.state = 'invoiced'
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_number_id = fields.Many2one('stock.production.lot', string='Batch Number',domain="[('product_id', '=', product_id)]")
