from datetime import datetime, date
from odoo import api, models, fields, _
from odoo.exceptions import UserError


class MedicalAppoimtments(models.Model):
    _name = 'medical.appointment'
    _inherit = ['mail.thread','resource.mixin','mail.activity.mixin']
    _description = 'Appointment Details'
    _order = 'id desc'

    new_patient_is = fields.Boolean("New Patient")
    patient_new = fields.Char(string='New Patient')



    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'patient_id' in vals:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'medical.appointment') or _('New')
            if vals.get('patient_new') and vals.get('new_patient_is'):
                patient = self.env['medical.patient'].create({'name': vals.get('patient_new'),
                                                              'no_idcode': False,
                                                              'street': vals.get('street'),
                                                              'city': vals.get('city'),
                                                              'patient_age': vals.get('age'),
                                                              'phone': vals.get('phone'),
                                                              'gender': vals.get('gender')})
                if patient:
                    vals['patient_id'] = patient.id

        return super(MedicalAppoimtments, self).create(vals)

    name = fields.Char(string='Appointment Reference', copy=False, readonly=True, index=True,
                       default=lambda self: _('New'), )

    so_wo = fields.Char(string='C/O', related='patient_id.so_wo')
    patient_id = fields.Many2one('medical.patient', string='Patient Name', required=True)

    phone = fields.Char('Contact Number', related='patient_id.phone')

    city = fields.Char(related='patient_id.city')

    zip = fields.Char(change_default=True, related='patient_id.zip')

    birthdate_date = fields.Date('Birth Date', related='patient_id.birthdate_date', required=True)

    street = fields.Char(related='patient_id.street')

    street2 = fields.Char(related='patient_id.street2')

    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', related='patient_id.state_id')

    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', related='patient_id.country_id')

    identification_code = fields.Char('File Number', related='patient_id.identification_code')

    date = fields.Date(default=fields.Date.context_today, )

    age = fields.Char('Age')

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
    search_file_number = fields.Char('Search File Number')
    registration_id = fields.Many2one('medical.opthalmology', string="Registration")

    @api.onchange('search_file_number')
    def _onchange_search_file_number(self):

        new = self.env['medical.patient'].search([('identification_code', '=', self.search_file_number)])
        for i in new:
            if i.identification_code:
                self.patient_id = i.id
                self.phone = i.phone
                self.email = i.email
                self.age = i.patient_age
                self.gender = i.gender
                self.street = i.street

    @api.onchange('phone')
    def _onchange_phone(self):
        if self.phone and not self.new_patient_is:

            new = self.env['medical.patient'].search([('phone', '=', self.phone)])
            for i in new:
                if i.phone:
                    self.patient_id = i.id
                    self.identification_code = i.identification_code
                    self.age = i.patient_age
                    self.gender = i.gender
                    self.street =i.street

    def create_registration(self):
        context = self.env.context.copy()
        if not self.appointment_date:
            raise UserError(
                _('Please define Appointment Date Which will be used as Registration Time'))
        if not self.phone:
            raise UserError(
                _('Please Add Contact Number'))
        else:
            date = datetime.strptime(self.appointment_date, "%Y-%m-%d").date()
            date_today = date.today()
            vals = {
                    'patient_id': self.patient_id.id,
                    'phone': self.phone,
                    'identification_code': self.identification_code,
                    'age': self.age,
                    'gender': self.gender,
                    'doctor_id': self.doctor_id.id,
                    'appointment_id' : self.id,

                }
            if self.new_patient_is:
                vals['new_patient_is'] = True
                vals['patient_new'] = self.patient_id.name

            res = self.env['medical.opthalmology'].create(vals)
            if res.appointment_id and res.new_patient_is:
                identification_code = res.patient_id.genarate_file_number()
                res.identification_code = identification_code
                res.patient_id.write({'identification_code': identification_code})
            self.state = 'confirmed'
            self.registration_id = res
            view = self.env.ref('medical_opthalmology.patient_appointment_tree').ids
            form_view_id = self.env.ref('medical_opthalmology.view_patient_appointment_form').ids

            # return {
            #     'type': 'ir.actions.act_window',
            #     'view_mode': 'tree,form',
            #     'res_model': 'medical.appointment',
            #     'views': [[view, 'tree'], [form_view_id, 'form']],
            #     'target': 'current',
            #     'context': {'search_default_state': 'registration'},
            # }
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('medical_opthalmology.view_patient_registration_form').id,
                'res_model': 'medical.opthalmology',
                'res_id': res.id,

            }
    def view_registration(self):
        return {
            'name': 'Registration',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'medical.opthalmology',
            'view_id': self.env.ref('medical_opthalmology.view_patient_registration_form').id,
            'target': 'current',
            'res_id': self.registration_id.id,
            'type': 'ir.actions.act_window',
        }
    @api.onchange('appointment_date')
    def _onchange_appointment_date(self):
        if self.appointment_date:
            date_appointment = datetime.strptime(self.appointment_date, "%Y-%m-%d").date()
            date_today = date.today()
            if date_appointment < date_today:
                raise UserError('Appointment date must be greater than current')

    def reset_sequence(self):
        sequences = self.env['ir.sequence'].search([('code','=','medical.appointment')],limit=1)
        sequences.write({'number_next_actual': 1})
