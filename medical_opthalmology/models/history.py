from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class History(models.Model):
    _inherit = 'medical.opthalmology'

    pre_regstr_history_ids = fields.Many2many('medical.opthalmology', 'current_record', 'previos_records',
                                              string='History', store=True)

    past_history_ids = fields.One2many('medical.opthalmology', 'patient_visit_id', string='Past History')

    patient_visit_id = fields.Many2one('medical.opthalmology')

    history = fields.Boolean('History', default=False)

    @api.model
    def create(self, vals):
        ids = []
        visit = self.env['medical.opthalmology'].search([('patient_id', '=', vals['patient_id'])])
        if len(visit) >= 1:
            for record in visit:
                record.patient_visit_id = record.id
                ids.append(record.id)
            vals.update({
                'past_history_ids': [(6, 0, ids)],
                'history': True,

            })

        return super(History, self).create(vals)
