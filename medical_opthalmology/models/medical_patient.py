from odoo import fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    past_history_ids = fields.One2many('medical.opthalmology', 'patient_id', string='Past History', readonly=True)
