from odoo import models, fields


class MedicalRefractionist(models.Model):
    _name = "medical.refractionist"

    name = fields.Char('Name', required=True)
    refractionist_id = fields.Char('ID')
