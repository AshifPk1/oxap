from odoo import api, models, fields, _


class VisualAcuity(models.Model):
    _name = 'visual.acuity'

    re = fields.Char('PG', store=True)
    le = fields.Char('UC', store=True)
    va = fields.Char(' ')
    selection = fields.Selection([
        ('snellen_chart', 'Snellen Chart'),
        ('cambridge_chart', 'Cambridge Chart'),
        ('e_chart', 'E-Chart')
    ], string=' ')
    pinhole = fields.Char('PH', store=True)
    patient_visit_re_id = fields.Many2one('medical.opthalmology', store=True)
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)

    def action_show_re(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')
        context = self.env.context.copy()

        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_re': True, 'default_le': False, 'default_va': False},
            'target': 'new',
        }

    def action_show_le(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')
        context = self.env.context.copy()

        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_le': True, 'default_va': False, 'default_re': False},
            'target': 'new',
        }


class IOP(models.Model):
    _name = 'optical.iop'

    head = fields.Char(' ', readonly=True)
    re = fields.Char('RE', store=True)
    le = fields.Char('LE', store=True)
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)


class UndialatedRefratcionOptics(models.Model):
    _name = 'undilated.refraction.optics'

    head = fields.Char(' ')
    sphere = fields.Char('Sph', store=True)
    cyl = fields.Char('Cyl', store=True)
    axis = fields.Char('Axis', store=True)
    va = fields.Char('V/A', store=True)
    patient_visit_id = fields.Many2one('medical.optics', store=True)


class DilatedRefratcionOptics(models.Model):
    _name = 'dilated.refraction.optics'

    head = fields.Char(' ')
    sphere = fields.Char('Sph', store=True)
    cyl = fields.Char('Cyl', store=True)
    axis = fields.Char('Axis', store=True)
    va = fields.Char('V/A', store=True)
    patient_visit_id = fields.Many2one('medical.optics', store=True)
    patient_visit_re_id = fields.Many2one('medical.optics', store=True)


class DilatedAR(models.Model):
    _name = 'dilated.ar'

    dilated_ar = fields.Char(' ')
    va = fields.Char(string='V/A', store=True)
    sphere = fields.Char(string='Sph', store=True)
    cyl = fields.Char(string='Cyl', store=True)
    axis = fields.Char(string='Axis', store=True)
    color_status = fields.Boolean(default=False)
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    patient_visit_re_id = fields.Many2one('medical.opthalmology', store=True)

    @api.onchange('sphere', 'cyl', 'axis', 'va')
    def on_change_list_values(self):
        if self.dilated_ar == 'NV' or self.dilated_ar == 'DV':
            if self.sphere or self.cyl or self.axis or self.va:
                self.color_status = True
            else:
                self.color_status = False
        else:
            self.color_status = False

    # @api.onchange('sphere','cyl','axis','va')
    def on_change_values(self):
        for record in self:
            if record.dilated_ar == 'NV' or record.dilated_ar == 'DV':
                record.color_status = True
            else:
                record.color_status = False

    @api.multi
    def action_show_sphere(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')
        context = self.env.context.copy()

        self.on_change_values()
        return {
            'name': _('Register Sphere Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_sphere': True},
            'target': 'new',
        }

    def action_show_cyl(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')
        context = self.env.context.copy()
        self.on_change_values()
        return {
            'name': _('Register Cyl Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_cyl': True},
            'target': 'new',
        }

    def action_show_axis(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_axis_view')
        context = self.env.context.copy()
        self.on_change_values()
        return {
            'name': _('Register Axis Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.axis',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_axis': True},
            'target': 'new',
        }

    def action_show_va(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')
        self.on_change_values()
        nv_is = False
        if self.dilated_ar == 'NV':
            nv_is = True
        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_va': True, 'default_nv': nv_is, 'default_le': False, 'default_re': False},
            'target': 'new',
        }


class Normalvalues(models.Model):
    _name = 'normal.eyevalues'

    r_eye = fields.Char('R Eye', store=True)
    l_eye = fields.Char('L Eye', store=True)
    catg = fields.Char(' ')
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)


class DrugAllergies(models.Model):
    _name = 'drug.allergies'
    drug_id = fields.Many2one('drug.drugs', 'Drug', required=True, store=True)
    allergies = fields.Char('Allergies', store=True)
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)


class Drugs(models.Model):
    _name = 'drug.drugs'
    name = fields.Char('Drugs', store=True)


class InvestigationsExamination(models.Model):
    _name = 'eye.investigations.examination'

    investigation = fields.Char('Investigations', required=True, store=True)
    r = fields.Char('R', store=True)
    l = fields.Char('L', store=True)
    yes = fields.Boolean(' ')
    time = fields.Date()
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)


class Investigations(models.Model):
    _name = 'eye.investigations'

    name = fields.Char('Investigations', store=True)


class OpticalInvestigations(models.Model):
    _name = 'optical.investigations'

    investigation = fields.Many2one('product.product', required=True,
                                    domain=['&', ('type', '=', 'service'), ('is_investigation', '=', True)])
    qty = fields.Float('Qty', default=1)
    date = fields.Date('Date')
    amount = fields.Float('Amount', force_save=True, store=True)
    space = fields.Char(' ', readonly=True, store=True)
    eye = fields.Selection([('left_eye', 'LE'), ('right_eye', 'RE'), ('both', 'BE')])
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    patient_visit_optics_id = fields.Many2one('medical.optics', store=True)
    tax_ids = fields.Many2many('account.tax', string='Tax', store=True, domain=[('type_tax_use', '=', 'sale')])
    price_tax = fields.Float(compute='_compute_amount', string='Taxes', readonly=True, store=True)
    discount = fields.Float('Discount', readonly=False, store=True)
    sub_total = fields.Float('Sub Total', compute='compute_sub_total')
    price_total = fields.Float(compute='_compute_amount', string='Total', readonly=True, store=True)
    instruction_id = fields.Many2many('investigation.instruction', String='Instruction')
    report = fields.Char('Report')

    @api.onchange('investigation')
    def _onchange_investigations(self):
        self.amount = self.investigation.list_price

    @api.depends('investigation', 'qty', 'amount')
    def compute_sub_total(self):
        for record in self:
            record.sub_total = (record.amount) * (record.qty)

    @api.depends('qty', 'discount', 'amount', 'tax_ids', )
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.amount * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.patient_visit_id.currency_id, line.qty,
                                             product=line.investigation, partner=False)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
            })


class Treatment(models.Model):
    _name = 'optical.treatment'

    patient_visit_id = fields.Many2one('medical.opthalmology')
    drug_id = fields.Many2one('product.product', string='Drug', required=True,
                              domain=['&', ('type', 'in', ['consu', 'product']), ('is_pharmacy', '=', True)])
    days = fields.Integer('Days')
    eye = fields.Selection([('left_eye', 'LE'), ('right_eye', 'RE')], String='Eye')
    frequency = fields.Char('Frequency', store=True)
    remarks = fields.Char('Remarks', store=True)


class Prescription(models.Model):
    _name = 'optical.prescription'

    patient_visit_id = fields.Many2one('medical.optics', store=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 domain=['|', ('is_lens', '=', True), ('is_frame', '=', True)])
    quantity = fields.Float('Qty', default=1, store=True)
    price_unit = fields.Float('Price Unit', store=True)
    tax_ids = fields.Many2many('account.tax', string='Tax')
    sub_total = fields.Float('Sub Total', compute='compute_sub_total', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Taxes', readonly=True, store=True)
    discount = fields.Float('Discount', readonly=True)
    price_total = fields.Float(compute='_compute_amount', string='Total', readonly=True, store=True)

    @api.depends('product_id', 'quantity', 'price_unit')
    def compute_sub_total(self):
        for record in self:
            record.sub_total = record.price_unit * (record.quantity)

    @api.onchange('product_id')
    def _onchange_product_ids(self):
        self.price_unit = self.product_id.list_price

    @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', )
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.patient_visit_id.currency_id, line.quantity,
                                             product=line.product_id, partner=False)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
            })


class PrescriptionOs(models.Model):
    _name = 'optical.prescription_os'

    patient_visit_id = fields.Many2one('medical.opthalmology')
    head_os = fields.Char(' ')
    sph_os = fields.Char('SPH', store=True)
    cyl_os = fields.Char('CYL', store=True)
    axis_os = fields.Char('AXIS', store=True)
    va_os = fields.Char('VA', store=True)


class Prescription_Drug(models.Model):
    _name = 'optical.prescription_drug'

    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    drug_id = fields.Many2one('product.product', string='Drug', required=True, store=True)
    days = fields.Integer('Days', store=True)
    eye = fields.Selection([('left_eye', 'LE'), ('right_eye', 'RE')], String='Eye')
    frequency = fields.Char('Frequency', store=True)
    remarks = fields.Char('Remarks', store=True)


class Lens(models.Model):
    _name = 'optical.lens'

    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    model = fields.Many2one('product.product', string='Brand', domain=[('is_surgery_lens', '=', True)])
    power = fields.Char('Power', store=True)
    item = fields.Char('Item', store=True)
    qty = fields.Float('Qty', default=1, store=True)
    rate = fields.Float('Amount', store=True)
    space = fields.Char(' ', readonly=True, store=True)

    @api.onchange('model')
    def on_change_mpdel(self):
        if self.model:
            self.power = self.model.power
            self.item = self.model.item


class OpticalIOL(models.Model):
    _name = 'optical.iol'

    iol = fields.Char('_', readonly=True, store=True)
    ref_err_1 = fields.Char('Ref.Err', store=True)
    power = fields.Char('Power', store=True)
    ref_err_2 = fields.Char('Ref.Err', store=True)
    power_2 = fields.Char('Power', store=True)
    constant = fields.Char('A Const.', store=True)

    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    patient_visit_re_id = fields.Many2one('medical.opthalmology', store=True)


class OpticalKeratometer(models.Model):
    _name = 'optical.keratometer'

    keratometer = fields.Char(' ', readonly=True, store=True)
    k1 = fields.Char(' ')
    k2 = fields.Char(' ')

    axis = fields.Char(' ')
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    patient_visit_re_id = fields.Many2one('medical.opthalmology', store=True)


class SurgeryItems(models.Model):
    _name = 'surgery.items'

    patient_visit_id = fields.Many2one('medical.opthalmology')

    name = fields.Char('Item', required=True, store=True)
    quantity = fields.Float('Quantity', store=True)


class OldGlassSub(models.Model):
    _name = 'old.glass.sub'

    old_glass_id = fields.Many2one('old.glass', ondelete='cascade', store=True)
    old_glass_re_id = fields.Many2one('old.glass', ondelete='cascade', store=True)
    head = fields.Char(' ', ondelete='cascade', store=True)
    sphere = fields.Char('SPH', ondelete='cascade', store=True)
    cyl = fields.Char('CYL', ondelete='cascade', store=True)
    axis = fields.Char('AXIS', ondelete='cascade', store=True)
    va = fields.Char('VA', ondelete='cascade', store=True)


class OldGlass(models.Model):
    _name = 'old.glass'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'patient_id' in vals:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'old.glass') or _('New')
                vals['name'] = vals['name']

        return super(OldGlass, self).create(vals)

    @api.model
    def default_old_glass_values(self):
        old_glass_list = ['DV', 'NV']
        ids = []
        for item in old_glass_list:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_old_glass_re_values(self):
        old_glass_list = ['DV', 'NV']
        ids = []
        for item in old_glass_list:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    name = fields.Char('Reference', required=True, default=lambda self: _('New'), readonly=True, store=True)
    old_glass_wizard_id = fields.Many2one('old.glass.wizard', store=True)
    old_glass_le_ids = fields.One2many('old.glass.sub', 'old_glass_id', string='Old Glass',
                                       default=default_old_glass_values, store=True)
    old_glass_re_ids = fields.One2many('old.glass.sub', 'old_glass_re_id', string='Old Glass',
                                       default=default_old_glass_re_values, store=True)
    glass_status = fields.Selection([
        ('available', 'Available'),
        ('previous', 'Previous')])

    glass_type = fields.Selection([
        ('bi_focal', 'Bifocal'),
        ('uni_focal', 'Unifocal'),
        ('progressive', 'Progressive'), ])

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


class CycloDetails(models.Model):
    _name = 'cyclo.details'

    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    patient_visit_re_id = fields.Many2one('medical.opthalmology', store=True)
    sphere = fields.Char('SPH', store=True)
    cyl = fields.Char('Cyl', store=True)
    axis = fields.Char('Axis', store=True)
    va = fields.Char('V/A', store=True)
    head = fields.Char(' ', readonly=True, store=True)

    def action_show_sphere(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')

        return {
            'name': _('Register Sphere Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_sphere': True},
            'target': 'new',
        }

    def action_show_cyl(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')

        return {
            'name': _('Register Cyl Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_cyl': True},
            'target': 'new',
        }

    def action_show_axis(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_axis_view')

        return {
            'name': _('Register Axis Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.axis',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_axis': True},
            'target': 'new',
        }

    def action_show_va(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')

        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_va': True, 'default_le': False, 'default_re': False},
            'target': 'new',
        }


class AlternateGlass(models.Model):
    _name = 'alternate.glass'

    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    patient_visit_re_id = fields.Many2one('medical.opthalmology', store=True)
    sphere = fields.Char('SPH', store=True)
    cyl = fields.Char('Cyl', store=True)
    axis = fields.Char('Axis', store=True)
    va = fields.Char('V/A', store=True)
    head = fields.Char(' ', readonly=True)

    def action_show_sphere(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')

        return {
            'name': _('Register Sphere Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_sphere': True},
            'target': 'new',
        }

    def action_show_cyl(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')

        return {
            'name': _('Register Cyl Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_cyl': True},
            'target': 'new',
        }

    def action_show_axis(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_axis_view')

        return {
            'name': _('Register Axis Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.axis',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_axis': True},
            'target': 'new',
        }

    def action_show_va(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')

        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_va': True, 'default_le': False, 'default_re': False},
            'target': 'new',
        }


class Axl(models.Model):
    _name = 'optical.axl'

    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    patient_visit_re_id = fields.Many2one('medical.opthalmology', store=True)
    contact = fields.Char('Contact', store=True)
    immersion = fields.Char('Immersion', store=True)
    corrected = fields.Char('Crrected', store=True)
    axl = fields.Char(' ', readonly=True, store=True)


class SurgeryPackage(models.Model):
    _name = 'surgery.package'

    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)
    surgery = fields.Many2one('product.product', 'Surgery Pkg', required=True, store=True,
                              domain=[('is_surgery_package', '=', True)])
    description = fields.Char('Description', store=True)
    amount = fields.Float('Amount', store=True)
    qty = fields.Float('Qty', default=1, store=True)
    space = fields.Char(' ', readonly=True, store=True)
    tax_ids = fields.Many2many('account.tax', string='Tax', store=True, domain=[('type_tax_use', '=', 'sale')])

    price_tax = fields.Float(compute='_compute_amount', string='Taxes', readonly=True, store=True)
    discount = fields.Float('Discount', readonly=False, store=True)
    sub_total = fields.Float('Sub Total', compute='compute_sub_total', store=True)
    price_total = fields.Float(compute='_compute_amount', string='Total', readonly=True, store=True)

    @api.onchange('surgery')
    def _onchange_surgery(self):
        self.amount = self.surgery.list_price

    @api.depends('surgery', 'qty', 'amount')
    def compute_sub_total(self):
        for record in self:
            record.sub_total = record.amount * record.qty

    @api.depends('qty', 'discount', 'amount', 'tax_ids', )
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.amount * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.patient_visit_id.currency_id, line.qty,
                                             product=line.surgery, partner=False)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
            })


class ReferenceFrom(models.Model):
    _name = 'reference.from'

    name = fields.Char('Reference From', required=True, store=True)
    type_id = fields.Many2one('reference.type', store=True)


class ReferenceType(models.Model):
    _name = 'reference.type'

    name = fields.Char('Reference Type', required=True, store=True)


class EyeValue(models.Model):
    _name = 'eye.value'

    name = fields.Char('Value', store=True)


class EyeValueMe(models.Model):
    _name = 'eye.value_me'

    name = fields.Char('Value', store=True)


class EyeValueRe(models.Model):
    _name = 'eye.value_re'

    name = fields.Char('Value', store=True)


class EyeValueRe_2(models.Model):
    _name = 'eye.value_re_2'

    name = fields.Char('Value', store=True)


class EyeValueAxis(models.Model):
    _name = 'eye.value_axis'

    name = fields.Char('Value', store=True)


class EyeValueAxisMe(models.Model):
    _name = 'eye.value_axis_me'

    name = fields.Char('Value', store=True)


class EyeValueAxisRe(models.Model):
    _name = 'eye.value_axis_re'

    name = fields.Char('Value', store=True)


class EyeValueAxisRe_2(models.Model):
    _name = 'eye.value_re_axis_2'

    name = fields.Char('Value', store=True)


class EyeValueVa(models.Model):
    _name = 'eye.value_va'

    name = fields.Char('Value', store=True)


class EyeValueVaMe(models.Model):
    _name = 'eye.value_va_me'

    name = fields.Char('Value', store=True)


class EyeValueVaRe(models.Model):
    _name = 'eye.value_va_re'

    name = fields.Char('Value', store=True)


class EyeValueVaRe_2(models.Model):
    _name = 'eye.value_re_va_2'

    name = fields.Char('Value', store=True)


class EyeValueReNVVa(models.Model):
    _name = 'eye.value_va_nv_re'

    name = fields.Char('Value', store=True)


class EyeValueRENVVA(models.Model):
    _name = 'eye.value_nv_re_va_2'

    name = fields.Char('Value', store=True)


class VisualAcuityLe(models.Model):
    _name = 'visual.acuity.le'

    re = fields.Char('PG', store=True)
    le = fields.Char('UC', store=True)
    va = fields.Char(' ')
    selection = fields.Selection([
        ('snellen_chart', 'Snellen Chart'),
        ('cambridge_chart', 'Cambridge Chart'),
        ('e_chart', 'E-Chart')
    ], string=' ')
    pinhole = fields.Char('PH', store=True)

    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)

    def action_show_re(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')

        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_re': True, 'default_le': False, 'default_va': False},
            'target': 'new',
        }

    def action_show_le(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')

        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_le': True, 'default_va': False, 'default_re': False},
            'target': 'new',
        }


class VisualAcuityRe(models.Model):
    _name = 'visual.acuity.re'

    re = fields.Char('PG', store=True)
    le = fields.Char('UC', store=True)
    va = fields.Char(' ')
    selection = fields.Selection([
        ('snellen_chart', 'Snellen Chart'),
        ('cambridge_chart', 'Cambridge Chart'),
        ('e_chart', 'E-Chart')
    ], string=' ')
    pinhole = fields.Char('PH', store=True)

    patient_visit_re_id = fields.Many2one('medical.opthalmology', store=True)

    def action_show_re(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')

        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_re': True, 'default_le': False, 'default_va': False},
            'target': 'new',
        }

    def action_show_le(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')

        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_le': True, 'default_va': False, 'default_re': False},
            'target': 'new',
        }


class DilatedARLe(models.Model):
    _name = 'dilated.ar.le'

    dilated_ar = fields.Char(' ')
    va = fields.Char(string='V/A', store=True)
    sphere = fields.Char(string='Sph', store=True)
    cyl = fields.Char(string='Cyl', store=True)
    axis = fields.Char(string='Axis', store=True)
    color_status = fields.Boolean(default=False)
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)

    @api.multi
    def action_show_sphere(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')
        context = self.env.context.copy()

        self.on_change_values()
        return {
            'name': _('Register Sphere Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_sphere': True},
            'target': 'new',
        }

    def action_show_cyl(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')
        self.on_change_values()
        return {
            'name': _('Register Cyl Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_cyl': True},
            'target': 'new',
        }

    def action_show_axis(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_axis_view')
        self.on_change_values()
        return {
            'name': _('Register Axis Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.axis',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_axis': True},
            'target': 'new',
        }

    def action_show_va(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')
        context = self.env.context.copy()
        self.on_change_values()
        nv_is = False
        if self.dilated_ar == 'NV':
            nv_is = True
        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_va': True, 'default_nv': nv_is, 'default_le': False, 'default_re': False},
            'target': 'new',
        }


class DilatedARRe(models.Model):
    _name = 'dilated.ar.re'

    dilated_ar = fields.Char(' ')
    va = fields.Char(string='V/A', store=True)
    sphere = fields.Char(string='Sph', store=True)
    cyl = fields.Char(string='Cyl', store=True)
    axis = fields.Char(string='Axis', store=True)
    color_status = fields.Boolean(default=False)
    patient_visit_re_id = fields.Many2one('medical.opthalmology', store=True)

    @api.multi
    def action_show_sphere(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')

        self.on_change_values()
        return {
            'name': _('Register Sphere Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_sphere': True},
            'target': 'new',
        }

    def action_show_cyl(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_view')
        self.on_change_values()
        return {
            'name': _('Register Cyl Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_cyl': True},
            'target': 'new',
        }

    def action_show_axis(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_axis_view')
        self.on_change_values()
        return {
            'name': _('Register Axis Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.axis',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_axis': True},
            'target': 'new',
        }

    def action_show_va(self):
        view = self.env.ref('medical_opthalmology.eye_value_wizard_va_view')
        self.on_change_values()
        nv_is = False
        if self.dilated_ar == 'NV':
            nv_is = True
        return {
            'name': _('Register Values'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'eye.values.wizard.va',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': {'default_va': True, 'default_nv': nv_is, 'default_le': False, 'default_re': False},
            'target': 'new',
        }


class DialataionTplus(models.Model):
    _name = 'dialataion.tplus'

    name = fields.Char(string='Name', required=True)


class InvestigationInstruction(models.Model):
    _name = 'investigation.instruction'

    name = fields.Char(string='Name', required=True)
