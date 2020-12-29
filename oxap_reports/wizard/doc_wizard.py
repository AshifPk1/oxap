
from odoo import models, fields, _, api


class ImportInvoiceWiz(models.TransientModel):
    _name = 'doc.analysis.wiz'
    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")
    doctor_id = fields.Many2one('medical.practitioner', string="Doctor")
    doctor_name = fields.Char('name')

    @api.multi
    def get_data(self):
        return self.env.ref('oxap_reports.patient_list_xlsx').report_action(self)
