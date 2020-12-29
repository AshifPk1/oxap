from datetime import datetime, date
from odoo import api, models, fields, _
from odoo.exceptions import UserError


class MedicalAppoimtments(models.Model):
    _name = 'medical.appointment'
    _description = 'Appointment Details'
    _order = 'id desc'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'patient_id' in vals:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'medical.appointment') or _('New')

        return super(MedicalAppoimtments, self).create(vals)

    name = fields.Char(string='Appointment Reference', copy=False, readonly=True, index=True,
                       default=lambda self: _('New'), )

    patient_id = fields.Many2one('medical.patient', string='Patient Name', required=True)

    phone = fields.Char('Contact Number', related='patient_id.phone', required=True)

    city = fields.Char(related='patient_id.city')

    zip = fields.Char(change_default=True, related='patient_id.zip')

    birthdate_date = fields.Date('Birth Date', related='patient_id.birthdate_date', required=True)

    street = fields.Char(related='patient_id.street')

    street2 = fields.Char(related='patient_id.street2')

    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', related='patient_id.state_id')

    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', related='patient_id.country_id')

    identification_code = fields.Char('File Number', related='patient_id.identification_code')

    date = fields.Date(default=fields.Date.context_today, )

    age = fields.Float('Age')

    tag_ids = fields.Many2many('patient.visit.tag', string='Tags', )

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], related='patient_id.gender')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')], string='Status',
        default='draft')

    appointment_date = fields.Date('Appointment Date', )

    appointment_time = fields.Float('Appointment Time', )

    doctor_id = fields.Many2one('medical.practitioner', string='Doctor', required=True)

    note = fields.Text('Note')

    doctor_review_date = fields.Char('Review After')

    last_visit_date = fields.Datetime(string='Last Visit Date')

    date_today = fields.Date('Date', default=fields.Date.context_today, readonly=True, ondelete='cascade')

    def create_registration(self):
        context = self.env.context.copy()
        if self.appointment_date == False:
            raise UserError(
                _('Please define Appointment Date Which will be used as Registration Time'))

        date = datetime.strptime(self.appointment_date, "%Y-%m-%d").date()
        date_today = date.today()
        self.env['medical.opthalmology'].create(
            {
                'patient_id': self.patient_id.id,
                'phone': self.phone,
                'identification_code': self.identification_code,
                'age': self.age,
                'gender': self.gender,
                'doctor_id': self.doctor_id.id,

            })
        self.state = 'confirmed'
        view = self.env.ref('medical_opthalmology.patient_appointment_tree').ids
        form_view_id = self.env.ref('medical_opthalmology.view_patient_appointment_form').ids

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'medical.appointment',
            'views': [[view, 'tree'], [form_view_id, 'form']],
            'target': 'current',
            'context': {'search_default_state': 'registration'},
        }

    # check appointment date greater than current date
    @api.onchange('appointment_date')
    def _onchange_appointment_date(self):
        if self.appointment_date:
            date_appointment = datetime.strptime(self.appointment_date, "%Y-%m-%d").date()
            date_today = date.today()
            if date_appointment < date_today:
                raise UserError('Appointment date must be greater than current')
