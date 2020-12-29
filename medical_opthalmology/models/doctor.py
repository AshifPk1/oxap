from odoo import api, models, fields, _
from datetime import datetime
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DoctorCheckup(models.Model):
    _inherit = 'medical.opthalmology'

    referred_to_surgery = fields.Boolean('Referred To Surgery')
    treatment_needed = fields.Boolean(default=False, compute='_compute_treatment_status')
    dilation_status = fields.Selection(
        [('dilation', 'Dialatation'), ('ref_dilation', 'Refractive Dialatation'),
         ('dilation_done', 'Dialatation Done')])
    dilation_start_time = fields.Datetime('Dialatation Start Time')
    counselling_text = fields.Text('Counselling Text')
    prescription = fields.Text('Prescription')
    cornea_le_is = fields.Boolean('Cornea')
    cornea_le = fields.Text('Cornea')
    lens_le_is = fields.Boolean('Lens')
    lens_le = fields.Text('')
    conjunctiva_is = fields.Boolean('Conjunctiva')
    conjunctiva = fields.Text()
    cornea_re_is = fields.Boolean('Cornea')
    cornea_re = fields.Text()
    lens_re_is = fields.Boolean('Lens')
    lens_re = fields.Text()
    lids_re_is = fields.Boolean('Lids')
    lids_re = fields.Text()
    lids_le_is = fields.Boolean('Lids')
    lids_le = fields.Text()
    iris_le_is = fields.Boolean('Iris')
    iris_le = fields.Text()
    iris_re_is = fields.Boolean('Iris')
    iris_re = fields.Text()

    conjunctiva_re_is = fields.Boolean('Conjunctiva')
    conjunctiva_re = fields.Text()
    ac_is = fields.Boolean('AC')
    ac = fields.Text()
    ac_re_is = fields.Boolean('AC')
    ac_re = fields.Text()
    pupil_is = fields.Boolean('Pupil')
    pupil = fields.Text()
    pupil_re_is = fields.Boolean('Pupil')
    pupil_re = fields.Text()
    other_is = fields.Boolean('Other')
    other = fields.Text()
    other_re_is = fields.Boolean('Other')
    other_re = fields.Text()
    fundus_macula_le_is = fields.Boolean('Fundus Macula')
    fundus_macula_le = fields.Text()
    fundus_macula_re_is = fields.Boolean('Fundus Macula')
    fundus_macula_re = fields.Text()
    send_to_optics = fields.Boolean('Send To Optics', default=False)
    send_to_pharmacy = fields.Boolean('Send To Pharamcy', default=False)
    consultation_finish = fields.Boolean('Consultation Finished', default=False)

    doc_optical_id = fields.Many2one('medical.optics', string='optics')

    eye_image = fields.Binary(string='Eye Image')

    dialataion_tplus_id = fields.Many2one('dialataion.tplus', string='Dialatation Type', required=True)

    # @api.depends('procedure_details_ids')
    # def _compute_counselling(self):
    #     for rec in self:
    #         if rec.procedure_details_ids:
    #             rec.referred_to_surgery = True
    #         else:
    #             rec.referred_to_surgery = False

    @api.onchange('procedure_details_ids')
    def _onchange_procedure_details_ids(self):
        for rec in self:
            if rec.procedure_details_ids:
                rec.referred_to_surgery = True
            else:
                rec.referred_to_surgery = False

    @api.multi
    def update_consultation(self):
        self.write({'state': 'consultation'})

    @api.depends('prescription', 'medicine_ids')
    def _compute_treatment_status(self):
        for rec in self:
            if rec.prescription or rec.medicine_ids:
                rec.treatment_needed = True
            else:
                rec.treatment_needed = False

    @api.model
    def default_investigation_details_id(self):
        ids = []
        for line in range(0, 0):
            data = {
                'investigation': self.investigation_details_ids.investigation,
                'eye': self.investigation_details_ids.eye,
                'date': self.investigation_details_ids.date,
                'amount': self.investigation_details_ids.amount
            }
            ids.append((0, 0, data))
        return ids

    investigation_details_ids = fields.One2many('optical.investigations', 'patient_visit_id',
                                                string='Investigation Details',
                                                default=default_investigation_details_id)

    @api.model
    def default_treatment_ids(self):
        ids = []
        for line in range(0, 0):
            data = {
                'drug_id': self.drug_id,
                'days': self.drugs_ids.days,
                'eye': self.drugs_ids.eye,
                'frequency': self.drugs_ids.frequency,
                'remarks': self.drugs_ids.remarks
            }
            ids.append((0, 0, data))
        return ids

    drugs_ids = fields.One2many('optical.treatment', 'patient_visit_id', string='Prescription',
                                default=default_treatment_ids)

    @api.multi
    def confirm_consultation_warning(self):
        view = self.env.ref('medical_opthalmology.doctor_cosultaion_warning_wizard_view')
        context = self.env.context.copy()
        self.consultation_finish = True
        sent_to_procedure = False
        # if self.edure_details_ids:
        #     sent_to_procedure = True
        return {
            'name': _('Warning'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'doctor.warning.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {
                'default_dilated_ar_le_dv': self.dilated_ar_le_dv, 'default_va_le_dv': self.va_le_dv,
                'default_sphere_le_dv': self.sphere_le_dv, 'default_cyl_le_dv': self.cyl_le_dv,
                'default_axis_le_dv': self.axis_le_dv, 'default_dilated_ar_le_nv': self.dilated_ar_le_nv,
                'default_va_le_nv': self.va_le_nv, 'default_sphere_le_nv': self.sphere_le_nv,
                'default_cyl_le_nv': self.cyl_le_nv, 'default_axis_le_nv': self.axis_le_nv,
                'default_dilated_ar_re_dv': self.dilated_ar_re_dv, 'default_va_re_dv': self.va_re_dv,
                'default_sphere_re_dv': self.sphere_re_dv, 'default_cyl_re_dv': self.cyl_re_dv,
                'default_axis_re_dv': self.axis_re_dv, 'default_dilated_ar_re_nv': self.dilated_ar_re_nv,
                'default_va_re_nv': self.va_re_nv, 'default_sphere_re_nv': self.sphere_re_nv,
                'default_cyl_re_nv': self.cyl_re_nv, 'default_axis_re_nv': self.axis_re_nv,
                'default_glass_status': self.glass_needed,
                'default_surgery_status': self.referred_to_surgery,
                'default_glass_description': self.glass_prescription,
                'default_counselling_text': self.counselling_text,
                'default_treatment_status': self.treatment_needed,
                'default_treatment_prescription': self.prescription,
                'default_medicine_ids': [(6, 0, self.medicine_ids.ids)],
                'defailt_kryptok_status': self.kryptok_status,
                'default_progressive_status': self.progressive_status,
                'default_executive_status': self.executive_status,
                'default_univis_status': self.univis_status,
                'default_plastic_status': self.plastic_status,
                'default_h_index_status': self.h_index_status,
                'default_white_status': self.white_status,
                'default_tint_status': self.tint_status,
                'default_photochromic_status': self.photochromic_status,
                'default_investigation_details_ids': [(6, 0, self.investigation_details_ids.ids)],
                'default_arc_status': self.arc_status,
                'default_procedure_details_ids': [(6, 0, self.procedure_details_ids.ids)],
                'default_sent_to_procedure': sent_to_procedure
            },
        }

    @api.multi
    def forward_consultation(self):
        view = self.env.ref('medical_opthalmology.forward_consultation_wizard_view')
        context = self.env.context.copy()
        if self.forward_needed:
            context = {'default_doctor_id': self.forwarded_doctor_id.id, 'default_from_doctor_id': self.doctor_id.id,
                       'default_forward_text': self.forward_text, 'default_forward_needed': True}
            return {
                'name': _('Forward'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'forward.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context,
            }
        else:
            return {
                'name': _('Forward'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'forward.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
            }

    @api.multi
    def sent_to_refractive_dilation(self):
        self.write({'state': 'refraction'})
        self.dilation_status = 'ref_dilation'
        self.dilation_start_time = datetime.now()

        view = self.env.ref('medical_opthalmology.doctor_checkup_tree').ids
        form_view_id = self.env.ref('medical_opthalmology.view_doctor_checking_form').ids

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'medical.opthalmology',
            'views': [[view, 'tree'], [form_view_id, 'form']],
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit', 'create': False, 'search_default_state': 'consultation',
                        'search_default_date_today': 'date_today'},
        }

    @api.multi
    def sent_to_dilation(self):
        if self.state == 'counselling':
            self.write({'state': 'consultation'})
        else:
            self.dilation_status = 'dilation'
            self.dilation_start_time = datetime.now()

            view = self.env.ref('medical_opthalmology.doctor_checkup_tree').ids
            form_view_id = self.env.ref('medical_opthalmology.view_doctor_checking_form').ids

            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'medical.opthalmology',
                'views': [[view, 'tree'], [form_view_id, 'form']],
                'target': 'current',
                'context': {'form_view_initial_mode': 'edit', 'create': False, 'search_default_state': 'consultation',
                            'search_default_date_today': 'date_today'},
            }

    def sent_to_dialataion_wizard(self):
        view = self.env.ref('medical_opthalmology.dialataion_tplus_wizard_view')
        return {
            'name': _('Warning'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'dialataion.tplus.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
        }

    def sent_to_refracted_dialataion_wizard(self):
        view = self.env.ref('medical_opthalmology.dialataion_tplus_wizard_view')
        return {
            'name': _('Warning'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'dialataion.tplus.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_refracted_dialatation': True},
            'target': 'new',
        }

    @api.multi
    def confirm_consultation(self):
        ids_re = []
        ids_le = []
        i = 0
        if self.investigation_details_ids:
            self.write({'procedure_type': 'investigation'})
            self.write({'state': 'procedure'})
        if self.dilation_status == 'dilation':
            self.write({'dilation_status': 'dilation_done'})
        if self.referred_to_surgery:
            self.write({'state': 'counselling'})
        else:
            if self.sent_to_procedure:
                self.write({'state': 'procedure'})

        if self.glass_needed:
            self.send_to_optics = True
            if self.state == 'consultation':
                self.write({'state': 'done'})
            if self.doc_optical_id and self.doc_optical_id.state == 'open':
                self.doc_optical_id.update({'glass_prescription': self.glass_prescription})
            elif not self.doc_pharmacy_id:
                nvdv_lines_le = {'le_dv': 'LEDV', 'le_nv': 'LENV'}
                for data in nvdv_lines_le:
                    if data == 'le_dv':
                        data_re = {
                            'sphere': self.sphere_le_dv,
                            'cyl': self.cyl_le_dv,
                            'axis': self.axis_le_dv,
                            'va': self.va_le_dv,
                            'head': self.dilated_ar_le_dv,
                            'patient_visit_re_id': self.id
                        }
                        ids_re.append((0, 0, data_re))
                    if data == 'le_nv':
                        data_re = {
                            'sphere': self.sphere_le_nv,
                            'cyl': self.cyl_le_nv,
                            'axis': self.axis_le_nv,
                            'va': self.va_le_nv,
                            'head': self.dilated_ar_le_nv,
                            'patient_visit_re_id': self.id
                        }
                        ids_re.append((0, 0, data_re))

                nvdv_lines_re = {'re_dv': 'REDV', 're_nv': 'RENV'}
                for data in nvdv_lines_re:
                    if data == 're_dv':
                        data_le = {
                            'sphere': self.sphere_re_dv,
                            'cyl': self.cyl_re_dv,
                            'axis': self.axis_re_dv,
                            'va': self.va_re_dv,
                            'head': self.dilated_ar_re_dv,
                            'patient_visit_id': self.id
                        }
                        ids_le.append((0, 0, data_le))
                    if data == 're_nv':
                        data_le = {
                            'sphere': self.sphere_re_nv,
                            'cyl': self.cyl_re_nv,
                            'axis': self.axis_re_nv,
                            'va': self.va_re_nv,
                            'head': self.dilated_ar_re_nv,
                            'patient_visit_id': self.id
                        }
                        ids_le.append((0, 0, data_le))

                new = self.env['medical.optics'].create({
                    'name': self.name,
                    'patient_id': self.patient_id.id,
                    'date': self.date,
                    'patient_visit_id': self.id,
                    'age': self.age,
                    'doctor_id': self.doctor_id.id,
                    'glass_prescription': self.glass_prescription,
                    'tag_ids': [(6, 0, self.tag_ids.ids)],
                    'dilated_refraction_ids': ids_re,
                    'dilated_refraction_le_ids': ids_le,
                    'state': 'open',
                    'reference_type_id': self.reference_type_id.id,
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

                })
                self.doc_optical_id = new.id
        if not self.send_to_optics and not self.send_to_pharmacy and not self.referred_to_surgery and not self.investigation_details_ids and not self.sent_to_procedure:
            self.write({'state': 'done'})
        view = self.env.ref('medical_opthalmology.doctor_checkup_tree').ids
        form_view_id = self.env.ref('medical_opthalmology.view_doctor_checking_form').ids

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'medical.opthalmology',
            'views': [[view, 'tree'], [form_view_id, 'form']],
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit', 'create': False, 'search_default_state': 'consultation',
                        'search_default_date_today': 'date_today'},
        }

    def print_prescription(self):
        if self.medicine_ids or self.prescription:
            return self.env.ref('medical_opthalmology.print_prescription_report').report_action(self)
        else:
            raise UserError("There is no medications data to print")

    def print_prescription_without_header(self):
        if self.medicine_ids or self.prescription:
            return self.env.ref('medical_opthalmology.print_prescription_report_without_header').report_action(self)
        else:
            raise UserError("There is no medications data to print")

    def send_to_refraction(self):
        self.write({'state': 'refraction'})

    def medicine_list(self):
        view = self.env.ref('medical_opthalmology.medicine_list_wizard_view')
        history = self.past_history_ids
        ids = []
        if history:
            medicine = history[0].medicine_ids
            for line in medicine:
                data = {
                    'product_id': line.product_id.id,
                    'days': line.days,
                    'eye': line.eye,
                    'stock': line.stock,
                    'frequency_id': line.frequency_id.id
                }
                ids.append(data)

        return {
            'name': _('Medications'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'medicine.list.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {
                'default_medicine_line_ids': [(0, 0, id) for id in ids],
                'default_parent_id': self.id
            }
        }
