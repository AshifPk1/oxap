from odoo import api, models, fields


class History(models.Model):
    _inherit = 'medical.opthalmology'

    pre_regstr_history_ids = fields.Many2many('medical.opthalmology', 'current_record', 'previos_records',
                                              string='History', store=True)

    past_history_ids = fields.One2many('medical.opthalmology', 'patient_visit_id', string='Past History')

    patient_visit_id = fields.Many2one('medical.opthalmology')

    history = fields.Boolean('History', default=False)

    review_date = fields.Date(string="Review Date")

    review_notes = fields.Text(string='Review Note')

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
