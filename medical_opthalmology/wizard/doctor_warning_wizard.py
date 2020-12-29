from odoo import models, fields


class DoctorWarningWizard(models.TransientModel):
    _name = 'doctor.warning.wizard'

    glass_status = fields.Boolean('Glass Needed')

    surgery_status = fields.Boolean('Counselling Needed')

    treatment_status = fields.Boolean('Treatment Status')

    glass_description = fields.Text('Glass Details')

    counselling_text = fields.Text('Counselling Note')

    treatment_prescription = fields.Text('Treatment Details')

    note = fields.Text('Review Note')

    one_week = fields.Boolean('1 Wk')
    two_week = fields.Boolean('2 Wk')
    one_month = fields.Boolean('1 Mnth')
    other = fields.Boolean('Other')
    review_text = fields.Char('Specify')

    medicine_ids = fields.Many2many('doctor.treatment', readonly=1)

    def confirm_values(self):
        record = self.env['medical.opthalmology'].search([('id', '=', self._context['active_id'])])
        record.update(
            {
                'glass_needed': self.glass_status,
                'referred_to_surgery': self.surgery_status,
                'treatment_needed': self.treatment_status,
                'glass_prescription': self.glass_description,
                'counselling_text': self.counselling_text,
                'prescription': self.treatment_prescription
            }
        )
        if self.one_week == True:
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

                })

        if self.two_week == True:
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

                })
        if self.other == True:
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

                })

        return record.confirm_consultation()
