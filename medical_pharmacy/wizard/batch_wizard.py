from odoo import models, api, fields, _
from odoo.exceptions import UserError


class BatchWizard(models.TransientModel):
    _name = 'batch.wizard'

    product_id = fields.Many2one('product.product', string="Product")
    batch_wizard_lines = fields.One2many('batch.wizard.line', 'batch_wizard_id', string='Batch Lines')

    @api.multi
    def run(self):
        count = 0
        for line in self.batch_wizard_lines:
            if line.applied:
                count += 1
            continue
        if count > 1:
            raise UserError(
                _(
                    "You can't select More than one Batch"))
        else:
            for line in self.batch_wizard_lines:
                if line.applied:
                    if line.status == 'expired':
                        raise UserError(
                            _(
                                "You can't select an expired Batch"))
                    else:
                        sale_order_line = self.env['pharmacy.prescription'].search(
                            [('id', '=', self._context['active_ids'][0])])
                        sale_order_line.update({
                            'lot_number_id': line.lot_id.id,

                        })
        return True


class BatchWizardLines(models.TransientModel):
    _name = 'batch.wizard.line'

    applied = fields.Boolean('Apply')
    lot_id = fields.Many2one('stock.production.lot', string='Batch Number')
    expiry_date = fields.Date(string='Expiry Date', store=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired')], string='Expiry Status')
    batch_wizard_id = fields.Many2one('batch.wizard', ondelete='cascade')
    quant_ids = fields.Many2many('stock.quant')
