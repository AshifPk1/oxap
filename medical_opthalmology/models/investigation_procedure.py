from odoo import api, models, fields, _


class DoctorCheckup(models.Model):
    _inherit = 'medical.opthalmology'

    image = fields.Binary(string='Image')
    investigation_comments = fields.Html('Comments', default=' ')
    is_investigation_procedure = fields.Boolean(default=False)
    is_sent_from_doctor = fields.Boolean()

    def sent_investigation_to_doctor(self):
        self.write({'state': 'consultation'})
        self.is_investigation_procedure = True

    def send_to_investigation_procedure(self):
        self.write({'state': 'investigation'})
        self.is_sent_from_doctor = True
