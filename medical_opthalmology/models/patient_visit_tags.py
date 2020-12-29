from odoo import models, fields


class PatientVisitTags(models.Model):
    _name = 'patient.visit.tag'

    name = fields.Char('Tag Name')
    color = fields.Char('Color Index')
