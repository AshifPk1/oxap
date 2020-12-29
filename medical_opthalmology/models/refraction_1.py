from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, _


class Refraction_1(models.Model):
    _inherit = 'medical.opthalmology'

    refraction_id = fields.Many2one('res.users', string="Refractionist")

    @api.model
    def default_acuity_values(self):
        acuity_list = ['_', '_']
        ids = []
        for item in acuity_list:
            data = {
                'va': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_acuity_values_re(self):
        acuity_list = ['_', '_']
        ids = []
        for item in acuity_list:
            data = {
                'va': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_pgpower_values(self):
        pg_power_list = ['_', '_', '_']
        ids = []
        for item in pg_power_list:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_dilatedar_values(self):
        dilated_ar_list = ['AR', 'DV', 'ADD', 'RS']
        ids = []
        for item in dilated_ar_list:
            data = {
                'dilated_ar': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_dilatedar_values_re(self):
        dilated_ar_list = ['AR', 'DV', 'ADD', 'RS']
        ids = []
        for item in dilated_ar_list:
            data = {
                'dilated_ar': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_keratometer_values(self):
        keratometer_re_list = ['K1', 'K2']
        ids = []
        for item in keratometer_re_list:
            data = {
                'keratometer': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_keratometer_values_re(self):
        keratometer_re_list = ['K1', 'K2']
        ids = []
        for item in keratometer_re_list:
            data = {
                'keratometer': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_old_glass_values(self):
        old_glass_list = ['DV', 'ADD']
        ids = []
        for item in old_glass_list:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_old_glass_values_re(self):
        old_glass_list = ['DV', 'ADD']
        ids = []
        for item in old_glass_list:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    presenting_complaints = fields.Text('Presenting Complaints', default=' ')
    muscle_balance = fields.Text(string='Muscle Balance', default=' ')
    glass_needed = fields.Boolean()
    glass_prescription = fields.Text(string='Glass Prescription', default=' ')
    state = fields.Selection([
        ('registration', 'Registration'),
        ('waiting', 'Waiting'),
        ('refraction', 'Refraction'),
        ('consultation', 'Consultation'),
        ('counselling', 'Counselling'),
        ('iol', 'IOL'),
        ('surgery', 'Surgery'),
        ('pharmacy', 'Pharmacy'),
        ('optics', 'Optics'),
        ('done', 'Done')], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange',
        ondelete='cascade', default='registration',
    )
    move_state = fields.Selection([
        ('registration', 'Registration'),
        ('refraction', 'Refraction'),
        ('consultation', 'Consultation'),
        ('counselling', 'Counselling'),
        ('surgery', 'Surgery'),
        ('done', 'Done')],
    )

    nv_add_le = fields.Selection([('0.25', '0.25'),
                                  ('0.5', '0.5'),
                                  ('0.75', '0.75'),
                                  ('1', '1'),
                                  ('1.25', '1.25'),
                                  ('1.5', '1.5'),
                                  ('1.75', '1.75'),
                                  ('2', '2'),
                                  ('2.25', '2.25'),
                                  ('2.5', '2.5'),
                                  ('2.75', '2.75'),
                                  ('3', '3'),
                                  ('3.25', '3.25'),
                                  ('3.5', '3.5'),
                                  ('3.75', '3.75'),
                                  ('4', '4')
                                  ], string='NV Add Value')
    nv_add_re = fields.Selection([('0.25', '0.25'),
                                  ('0.5', '0.5'),
                                  ('0.75', '0.75'),
                                  ('1', '1'),
                                  ('1.25', '1.25'),
                                  ('1.5', '1.5'),
                                  ('1.75', '1.75'),
                                  ('2', '2'),
                                  ('2.25', '2.25'),
                                  ('2.5', '2.5'),
                                  ('2.75', '2.75'),
                                  ('3', '3'),
                                  ('3.25', '3.25'),
                                  ('3.5', '3.5'),
                                  ('3.75', '3.75'),
                                  ('4', '4')
                                  ], string='NV Add Value')

    visual_acuitity_l_ids = fields.One2many('visual.acuity.le', 'patient_visit_id', string='Visual Acuity',
                                            default=default_acuity_values)
    visual_acuitity_r_ids_re = fields.One2many('visual.acuity.re', 'patient_visit_re_id', string='Visual Acuity RE',
                                               default=default_acuity_values_re)

    dilated_ar_l_ids = fields.One2many('dilated.ar.le', 'patient_visit_id', string='Dilated AR',
                                       default=default_dilatedar_values)
    dilated_ar_re_r_ids = fields.One2many('dilated.ar.re', 'patient_visit_re_id', string='Dilated AR',
                                          default=default_dilatedar_values_re)

    visual_acuitity_ids = fields.One2many('visual.acuity', 'patient_visit_id', string='Visual Acuity',
                                          default=default_acuity_values)
    visual_acuitity_ids_re = fields.One2many('visual.acuity', 'patient_visit_re_id', string='Visual Acuity RE',
                                             default=default_acuity_values_re)

    dilated_ar_ids = fields.One2many('dilated.ar', 'patient_visit_id', string='Dilated AR',
                                     default=default_dilatedar_values)
    dilated_ar_re_ids = fields.One2many('dilated.ar', 'patient_visit_re_id', string='Dilated AR',
                                        default=default_dilatedar_values_re)
    new_details = fields.Boolean(defaul=False)

    doctor_findings = fields.Text('Findings')

    pinhole = fields.Char('Pin Hole', default=' ')
    pinhole_re = fields.Char('Pin Hole', default=' ')

    colour_le = fields.Char('Colour Vision', default=' ')
    colour_re = fields.Char('Colour Vision', default=' ')

    keratometer_ids = fields.One2many('optical.keratometer', 'patient_visit_id', string='Extra Info1',
                                      default=default_keratometer_values)
    keratometer_re_ids = fields.One2many('optical.keratometer', 'patient_visit_re_id', string='Extra Info2',
                                         default=default_keratometer_values_re)

    prism_le_1 = fields.Char(' ', default=' ')
    prism_le_2 = fields.Char(' ', default=' ')
    prism_re_1 = fields.Char(' ', default=' ')
    prism_re_2 = fields.Char(' ', default=' ')

    iop_st_le = fields.Char('', default=' ')
    iop_at_le = fields.Char('', default=' ')
    iop_nct_le = fields.Char('', default=' ')
    iop_st_re = fields.Char('', default=' ')
    iop_at_re = fields.Char('', default=' ')
    iop_nct_re = fields.Char('', default=' ')

    vertex_dist = fields.Char()
    ipd = fields.Char('IPD', default=' ')
    flag = fields.Boolean('Flag')

    @api.multi
    def sent_to_doctor(self):
        self.write({'state': 'consultation'})
        view = self.env.ref('medical_opthalmology.patient_revisit_view_tree').ids
        form_view_id = self.env.ref('medical_opthalmology.patient_revisit_view_form').ids
        if self.dilation_status == 'ref_dilation':
            self.write({'dilation_status': 'dilation_done'})
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'medical.opthalmology',
            'views': [[view, 'tree'], [form_view_id, 'form']],
            'context': {'form_view_initial_mode': 'edit', 'create': False, 'search_default_date_today': 'date_today',
                        'search_default_state': 'state'},
            'target': 'current',
        }

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.phone = self.patient_id.phone
        self.identification_code = self.patient_id.identification_code
        self.gender = self.patient_id.gender
        self.street = self.patient_id.street
        product = self.env['product.product'].search([('product_tmpl_id', '=', 1)], limit=1)
        self.registration_amount = product.list_price
        values = {

            'pricelist_id': self.patient_id.partner_id.property_product_pricelist and self.patient_id.partner_id.property_product_pricelist.id or False,
        }
        self.update(values)

        previous_records = self.env['medical.opthalmology'].search(
            [('registration_amount', '>', 0), ('patient_id', '=', self.patient_id.id), ('state', '!=', 'registration')])
        last_record = previous_records.sorted(key=lambda x: x.date or None, reverse=True)
        if last_record:
            if last_record[0].date:
                date = datetime.strptime(last_record[0].date, "%Y-%m-%d %H:%M:%S").date()
                date_today = date.today()
                r = relativedelta(date_today, date, )
                last_admission = (date_today - date).days
                self.last_payment_date = date
                self.last_payment_days = str(last_admission) + ' ' + 'Days before'

        visit = self.env['medical.opthalmology'].search([('patient_id', '=', self.patient_id.id)])
        if len(visit) >= 1:
            pre_ids = []
            for record in visit:
                record.patient_visit_id = record.id
                pre_ids.append(record.id)
            if not pre_ids == []:
                self.pre_regstr_history_ids = pre_ids

    @api.onchange('glass_prescription')
    def _onchange_glass_prescription(self):
        if self.glass_prescription:
            self.glass_needed = True
        else:
            self.glass_needed = False

    @api.onchange('phone')
    def _onchange_phone(self):
        if self.phone and not self.new_patient_is and not self.identification_code:

            patient_ids = self.env['medical.patient'].search([('phone', '=', self.phone)])
            if patient_ids:
                patient_id = patient_ids[0]
                self.patient_id = patient_id.id
                self.identification_code = patient_id.identification_code
                self.email = patient_id.email
                self.age = patient_id.patient_age
                self.gender = patient_id.gender
                self.street = patient_id.street
                return {'domain': {'patient_id': [('id', '=', patient_ids.ids)]}}

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

    @api.multi
    def refraction(self):
        self.write({'state': 'refraction'})

    @api.multi
    def action_view_old_glasses(self):
        view = self.env.ref('medical_opthalmology.old_glass_wizard_view')
        context = self.env.context.copy()
        record = self.env['old.glass.wizard'].search([('patient_id', '=', self.patient_id.id)], limit=1)
        self.flag = False
        if record:
            record.update(
                {'dilated_ar_le_dv': self.dilated_ar_le_dv, 'va_le_dv': self.va_le_dv,
                 'sphere_le_dv': self.sphere_le_dv, 'cyl_le_dv': self.cyl_le_dv,
                 'axis_le_dv': self.axis_le_dv, 'dilated_ar_le_nv': self.dilated_ar_le_nv,
                 'va_le_nv': self.va_le_nv, 'sphere_le_nv': self.sphere_le_nv,
                 'cyl_le_nv': self.cyl_le_nv, 'axis_le_nv': self.axis_le_nv,
                 'dilated_ar_re_dv': self.dilated_ar_re_dv, 'va_re_dv': self.va_re_dv,
                 'sphere_re_dv': self.sphere_re_dv, 'cyl_re_dv': self.cyl_re_dv,
                 'axis_re_dv': self.axis_re_dv, 'dilated_ar_re_nv': self.dilated_ar_re_nv,
                 'va_re_nv': self.va_re_nv, 'sphere_re_nv': self.sphere_re_nv,
                 'cyl_re_nv': self.cyl_re_nv, 'axis_re_nv': self.axis_re_nv
                 }
            )
            for item in record:
                if item.patient_visit_id.id == self.id:
                    self.flag = True
                    return {

                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'old.glass.wizard',
                        'target': 'new',
                        'context': context,
                        'res_id': item.id,
                    }
            if not self.flag:
                return {
                    'name': _('Old Glass Details'),
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'old.glass.wizard',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    'target': 'new',
                    'res_id': record.id,
                }
        else:
            data = {
                'name': _('Old Glass Details'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'old.glass.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': {
                    'default_name': self.name,
                    'default_patient_id': self.patient_id.id,
                    'default_identification_code': self.patient_id.identification_code,
                    'default_date': self.date,
                    'default_age': self.age,
                    'default_patient_visit_id': self.id,
                    'default_dilated_ar_le_dv': self.dilated_ar_le_dv, 'default_va_le_dv': self.va_le_dv,
                    'default_sphere_le_dv': self.sphere_le_dv, 'default_cyl_le_dv': self.cyl_le_dv,
                    'default_axis_le_dv': self.axis_le_dv, 'default_dilated_ar_le_nv': self.dilated_ar_le_nv,
                    'default_va_le_nv': self.va_le_nv, 'default_sphere_le_nv': self.sphere_le_nv,
                    'default_cyl_le_nv': self.cyl_le_nv, 'default_axis_le_nv': self.axis_le_nv,
                    'default_dilated_ar_re_dv': self.dilated_ar_re_dv, 'default_va_re_dv': self.va_re_dv,
                    'default_sphere_re_dv': self.sphere_re_dv, 'default_cyl_re_dv': self.cyl_re_dv,
                    'default_axis_re_dv': self.axis_re_dv, 'default_dilated_ar_re_nv': self.dilated_ar_re_nv,
                    'default_va_re_nv': self.va_re_nv, 'default_sphere_re_nv': self.sphere_re_nv,
                    'default_cyl_re_nv': self.cyl_re_nv, 'default_axis_re_nv': self.axis_re_nv
                },
            }
            return data
