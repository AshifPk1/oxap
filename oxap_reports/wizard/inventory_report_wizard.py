from odoo import models, fields, _, api


class ImportInvoiceWiz(models.TransientModel):
    _name = 'inventory.report.wiz'
    section = fields.Many2many('product.category'
                               , string="Select Product Category")

    @api.multi
    def get_data(self):
        # @api.multi
        # def print_report_xlsx(self):
        #     # data = {'date_from': self.date_from,
        #     #         'date_to': self.date_to,
        #     #         'wiz_id': self.id}

        return self.env.ref('oxap_reports.inventory_valuation_report_xlsx').report_action(self)