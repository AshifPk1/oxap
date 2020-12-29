from odoo import models, fields


class PatientVisitTags(models.Model):
    _name = 'patient.visit.tag'

    name = fields.Char('Tag Name')
    color = fields.Char('Color Index')
    presenting_complaints = fields.Char('Presenting Complaints')
    hop_i = fields.Char('HOP.I')
    medical_history = fields.Char('Medical History')
    surgical_history = fields.Char('Surgical History')
