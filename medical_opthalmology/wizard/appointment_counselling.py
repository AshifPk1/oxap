from odoo import models, fields


class CounsellingAppointment(models.TransientModel):
    _name = 'counselling.appointment'

    note = fields.Text('Review Note')
    one_week = fields.Boolean('1 Wk')
    two_week = fields.Boolean('2 Wk')
    one_month = fields.Boolean('1 Mnth')
    review_date = fields.Date('Review Date')
    other = fields.Boolean('Other')
    review_text = fields.Char('Specify')

    def confirm_values(self):

        if self.one_week:
            record = self.env['medical.opthalmology'].search([('id', '=', self._context['active_id'])])
            self.env['medical.appointment'].create(
                {
                    'patient_id': record.patient_id.id,
                    'phone': record.phone,
                    'identification_code': record.identification_code,
                    'age': record.age,
                    'gender': record.gender,
                    'doctor_id': record.doctor_id.id,
                    'note': self.note,
                    'doctor_review_date': 'After 1 Week',
                    'last_visit_date': record.date,

                })

        if self.two_week:
            record = self.env['medical.opthalmology'].search([('id', '=', self._context['active_id'])])
            self.env['medical.appointment'].create(
                {
                    'patient_id': record.patient_id.id,
                    'phone': record.phone,
                    'identification_code': record.identification_code,
                    'age': record.age,
                    'gender': record.gender,
                    'doctor_id': record.doctor_id.id,
                    'note': self.note,
                    'doctor_review_date': 'After 2 Week',
                    'last_visit_date': record.date,

                })

        if self.one_month == True:
            record = self.env['medical.opthalmology'].search([('id', '=', self._context['active_id'])])
            self.env['medical.appointment'].create(
                {
                    'patient_id': record.patient_id.id,
                    'phone': record.phone,
                    'identification_code': record.identification_code,
                    'age': record.age,
                    'gender': record.gender,
                    'doctor_id': record.doctor_id.id,
                    'note': self.note,
                    'doctor_review_date': 'After 1 Month',
                    'last_visit_date': record.date,

                })
        if self.review_date:
            record = self.env['medical.opthalmology'].search([('id', '=', self._context['active_id'])])
            self.env['medical.appointment'].create(
                {
                    'patient_id': record.patient_id.id,
                    'phone': record.phone,
                    'identification_code': record.identification_code,
                    'age': record.age,
                    'gender': record.gender,
                    'doctor_id': record.doctor_id.id,
                    'note': self.note,
                    'doctor_review_date': self.review_date,
                    'appointment_date': self.review_date
                })
        if self.other:
            record = self.env['medical.opthalmology'].search([('id', '=', self._context['active_id'])])
            self.env['medical.appointment'].create(
                {
                    'patient_id': record.patient_id.id,
                    'phone': record.phone,
                    'identification_code': record.identification_code,
                    'age': record.age,
                    'gender': record.gender,
                    'doctor_id': record.doctor_id.id,
                    'note': self.note,
                    'doctor_review_date': self.review_text,
                    'last_visit_date': record.date,

                })
