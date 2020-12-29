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
    review_date = fields.Date('Review Date')

    medicine_ids = fields.Many2many('doctor.treatment', readonly=1)
    sent_to_procedure = fields.Boolean(default=False)
    investigation_details_ids = fields.Many2many('optical.investigations', string='Investigation Details', readonly=1)
    procedure_details_ids = fields.Many2many('optical.procedure', string='Procedure Details', readonly=1)
    kryptok_status = fields.Boolean('Kryptok')
    progressive_status = fields.Boolean('Progressive')
    executive_status = fields.Boolean('Executive')
    univis_status = fields.Boolean('Univis D')
    plastic_status = fields.Boolean('Plastic')
    h_index_status = fields.Boolean('H Index')
    white_status = fields.Boolean('White')
    tint_status = fields.Boolean('Tint')
    photochromic_status = fields.Boolean('Photochromic')
    arc_status = fields.Boolean('ARC')
    special_instructions = fields.Text('Special Instructions')

    # DV
    dilated_ar_le_dv = fields.Char(' ', default='DV')
    va_le_dv = fields.Char(string='V/A', store=True)
    sphere_le_dv = fields.Char(string='Sph', store=True)
    cyl_le_dv = fields.Char(string='Cyl', store=True)
    axis_le_dv = fields.Char(string='Axis', store=True)

    # NV
    dilated_ar_le_nv = fields.Char(' ', default='ADD')
    va_le_nv = fields.Char(string='V/A', store=True)
    sphere_le_nv = fields.Char(string='Sph', store=True)
    cyl_le_nv = fields.Char(string='Cyl', store=True)
    axis_le_nv = fields.Char(string='Axis', store=True)

    # DV
    dilated_ar_re_dv = fields.Char(' ', default='DV')
    va_re_dv = fields.Char(string='V/A', store=True)
    sphere_re_dv = fields.Char(string='Sph', store=True)
    cyl_re_dv = fields.Char(string='Cyl', store=True)
    axis_re_dv = fields.Char(string='Axis', store=True)
    # NV
    dilated_ar_re_nv = fields.Char(' ', default='ADD')
    va_re_nv = fields.Char(string='V/A', store=True)
    sphere_re_nv = fields.Char(string='Sph', store=True)
    cyl_re_nv = fields.Char(string='Cyl', store=True)
    axis_re_nv = fields.Char(string='Axis', store=True)

    def confirm_values(self):
        record = self.env['medical.opthalmology'].search([('id', '=', self._context['active_id'])])
        record.update(
            {
                'glass_needed': self.glass_status,
                'referred_to_surgery': self.surgery_status,
                'sent_to_procedure': self.sent_to_procedure,
                'treatment_needed': self.treatment_status,
                'glass_prescription': self.glass_description,
                'counselling_text': self.counselling_text,
                'prescription': self.treatment_prescription,
                'sphere_le_dv': self.sphere_le_dv,
                'cyl_le_dv': self.cyl_le_dv,
                'axis_le_dv': self.axis_le_dv,
                'va_le_dv': self.va_le_dv,
                'sphere_le_nv': self.sphere_le_nv,
                'cyl_le_nv': self.cyl_le_nv,
                'axis_le_nv': self.axis_le_nv,
                'va_le_nv': self.va_le_nv,
                'sphere_re_dv': self.sphere_re_dv,
                'cyl_re_dv': self.cyl_re_dv,
                'axis_re_dv': self.axis_re_dv,
                'va_re_dv': self.va_re_dv,
                'sphere_re_nv': self.sphere_re_nv,
                'cyl_re_nv': self.cyl_re_nv,
                'axis_re_nv': self.axis_re_nv,
                'va_re_nv': self.va_re_nv,
                'kryptok_status': self.kryptok_status,
                'progressive_status': self.progressive_status,
                'executive_status': self.executive_status,
                'univis_status': self.univis_status,
                'plastic_status': self.plastic_status,
                'h_index_status': self.h_index_status,
                'white_status': self.white_status,
                'tint_status': self.tint_status,
                'photochromic_status': self.photochromic_status,
                'arc_status': self.arc_status,
                'special_instructions': self.special_instructions,
                'review_date':self.review_date,
                'review_notes':self.note

            }
        )

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
                    # 'doctor_review_date': self.review_date,
                    'appointment_date': self.review_date
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
                })

        if self.one_month:
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

                })
        return record.confirm_consultation()
