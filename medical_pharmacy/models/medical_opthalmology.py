from odoo import models, fields


class Doctor(models.Model):
    _inherit = 'medical.opthalmology'

    doc_pharmacy_id = fields.Many2one('medical.pharmacy', string='Pharmacy')

    def confirm_consultation(self):
        res = super(Doctor, self).confirm_consultation()
        if self.treatment_needed:
            self.send_to_pharmacy = True
            if self.state == 'consultation':
                self.write({'state': 'done'})
            if self.doc_pharmacy_id and self.doc_pharmacy_id.state == False:
                self.doc_pharmacy_id.update({'doctor_prescription': self.prescription})
            elif not self.doc_pharmacy_id:
                new = self.env['medical.pharmacy'].create({
                    'name': self.name,
                    'patient_id': self.patient_id.id,
                    'date': self.date,
                    'patient_visit_id': self.id,
                    'age': self.age,
                    'doctor_id': self.doctor_id.id,
                    'doctor_prescription': self.prescription,
                    'medicine_ids': [(6, 0, self.medicine_ids.ids)],
                    'tag_ids': [(6, 0, self.tag_ids.ids)],
                    'referred_by_id': self.referred_by_id.id,
                    'reference_type_id': self.reference_type_id.id,
                    're_state': 'processed',
                    'state': 'draft',
                    'treatment_status': True

                })
                self.doc_pharmacy_id = new.id
        return res


class DoctorTreatment(models.Model):
    _inherit = 'doctor.treatment'

    pharmacy_id = fields.Many2one('medical.pharmacy')
