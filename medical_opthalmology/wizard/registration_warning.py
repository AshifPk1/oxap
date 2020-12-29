from odoo import models, fields


class RegistrationWarningWizard(models.TransientModel):
    _name = 'registration.warning.wizard'

    last_payment_date = fields.Char('Last Payment Date', readonly=True)

    registration_amount = fields.Char('Registration Fee')

    patient_id = fields.Many2one('medical.patient', readonly=True, string='Patient Name', required=True, )

    doctor_id = fields.Many2one('medical.practitioner', string='Doctor', required=True, )

    identification_code = fields.Char('File Number', readonly=True, )

    journal_id = fields.Many2one('account.journal', 'Payment Method', domain="[('type', 'in', ['cash','bank'])]")

    phone = fields.Char('Contact Number', )

    state = fields.Selection([
        ('refraction', 'Refraction'),
        ('consultation', 'Consultation'),
        ('counselling', 'Counselling'),
        ('surgery', 'Surgery'),
        ('done', 'Done')],
    )

    def confirm_values(self):
        record = self.env['medical.opthalmology'].search([('id', '=', self._context['active_id'])])
        if self.state:
            state = self.state
        else:

            state = 'registration'
        record.update(
            {
                'registration_amount': self.registration_amount,
                'patient_id': self.patient_id,
                'doctor_id': self.doctor_id,
                'identification_code': self.identification_code,
                'journal_id': self.journal_id.id,
                'move_state': state
            }
        )
        record.confirm()
