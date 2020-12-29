from odoo import models, api


class MedicalReport(models.AbstractModel):
    _name = 'report.medical_opthalmology.medical_report_template_call'

    @api.multi
    def get_report_values(self, docids, data=None):
        eye_details = self.env['medical.opthalmology'].search([('id', '=', data['datas'])])

        dict1 = {}
        for rec in eye_details:
            dict1 = {
                'patient_id': rec.patient_id.partner_id.name,
                'identification_code': rec.patient_id.identification_code,
                'age': rec.patient_id.patient_age,
                'doctor': rec.doctor_id.name,
                'date': rec.date,
                'gender': rec.patient_id.gender,
                'pre_complaints': rec.presenting_complaints,
                'cornea_re': rec.cornea_re,
                'lens_re': rec.lens_re,
                'conjunctiva_re': rec.conjunctiva_re,
                'ac_re': rec.ac_re,
                'pupil_re': rec.pupil_re,
                'other_re': rec.other_re,
                'fundus_macula_re': rec.fundus_macula_re,
                'cornea_le': rec.cornea_le,
                'lens_le': rec.lens_le,
                'conjunctiva': rec.conjunctiva,
                'ac': rec.ac,
                'pupil': rec.pupil,
                'other': rec.other,
                'fundus_macula_le': rec.fundus_macula_le,
                'prescription': rec.prescription,
                'counselling_details': rec.counselling_details,
                'le_re': rec.ucdv_l_le,
                'pinhole_re': rec.ucdv_l_pinhole,
                'le_le': rec.ucdv_r_le,
                'pinhole_le': rec.ucdv_r_pinhole

            }
            return dict1
