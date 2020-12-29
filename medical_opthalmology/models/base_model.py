from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PatientRevisit(models.Model):
    _name = 'medical.opthalmology'
    _description = 'Medical Ophthalmology'
    _order = 'sequence desc'

    name = fields.Char(string='Patient Reference', required=True, copy=False, readonly=True, index=True,
                       ondelete='cascade', default=lambda self: _('New'), )

    patient_id = fields.Many2one('medical.patient', string='Patient Name', required=True, ondelete='cascade',
                                 states={'registration': [('readonly', False)]}, )
    appointment_id = fields.Many2one('medical.appointment')
    new_patient_is = fields.Boolean('New Patient')

    patient_new = fields.Char(string='New Patient')

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=False,
                                   help="Pricelist for current sales order.", default=1)

    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True,
                                  required=True)

    street = fields.Char(related='patient_id.street', string='Address')
    street2 = fields.Char(related='patient_id.street2')
    zip = fields.Char(change_default=True, related='patient_id.zip')
    city = fields.Char(related='patient_id.city', string='Place')
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', related='patient_id.state_id')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', related='patient_id.country_id')

    birthdate_date = fields.Date('Birth Date', related='patient_id.birthdate_date', required=True)

    phone = fields.Char('Contact Number', required=True, ondelete='cascade', related='patient_id.phone')

    identification_code = fields.Char('File Number', readonly=True, ondelete='cascade', store=True)

    referred_by_id = fields.Many2one('reference.from', 'Reference From')

    reference_type_id = fields.Many2one('reference.type', 'Reference Type')

    age = fields.Char(
        string='Age', related='patient_id.patient_age'
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], ondelete='cascade')

    date_reg = fields.Date('date reg')

    date = fields.Datetime('Admission Date', default=fields.Datetime.now, readonly=True, ondelete='cascade')

    date_today = fields.Date('Date', default=fields.Date.context_today, readonly=True, ondelete='cascade')

    doctor_id = fields.Many2one('medical.practitioner', string='Doctor', required=True, ondelete='cascade')

    forwarded_doctor_id = fields.Many2one('medical.practitioner', string='Forward Doctor', ondelete='cascade')

    forward_needed = fields.Boolean('Forward Needed')

    forward_status = fields.Selection([
        ('forwarded', 'Forwarded'),
        ('not_forwarded', 'Not Forwarded')], string='Forward Status')

    forward_text = fields.Text('Forward Text')

    registartion_invoice_id = fields.Many2one('account.invoice')

    is_deceased = fields.Boolean(
        compute='_compute_is_deceased',
    )

    counselling_invoice_id = fields.Many2one('account.invoice')

    invoiced_investigation = fields.Boolean('Investigation Invoiced', default=False)

    surgery_invoice_id = fields.Many2one('account.invoice')

    invoiced_surgery = fields.Boolean('Investigation Surgery', default=False)

    patient_diagnosis = fields.Text(string='Patient Diagnosis')

    so_wo = fields.Char(string='C/O', related='patient_id.so_wo')
    # visual_acuitity_l_ids fields

    ucdv_l_re = fields.Char('PG', store=True, default=' ')
    ucdv_l_le = fields.Char('UC', store=True, default=' ')
    ucdv_l_va = fields.Char(' ', readonly=True, default='-')
    ucdv_l_selection = fields.Selection([
        ('snellen_chart', 'Snellen Chart'),
        ('cambridge_chart', 'Cambridge Chart'),
        ('e_chart', 'E-Chart')
    ], string=' ')
    ucdv_l_pinhole = fields.Char('PH', store=True)
    ucdv_l_cl = fields.Char('CL', store=True, default=' ')

    ucnv_l_re = fields.Char('PG', store=True, default=' ')
    ucnv_l_le = fields.Char('UC', store=True, default=' ')
    ucnv_l_va = fields.Char(' ', readonly=True, default='-')
    ucnv_l_selection = fields.Selection([
        ('snellen_chart', 'Snellen Chart'),
        ('cambridge_chart', 'Cambridge Chart'),
        ('e_chart', 'E-Chart')
    ], string=' ')
    ucnv_l_pinhole = fields.Char('PH', store=True, default=' ')
    ucnv_l_cl = fields.Char('CL', store=True, default=' ')

    # visual_acuitity_r_ids_re fields

    ucdv_r_re = fields.Char('PG', store=True)
    ucdv_r_le = fields.Char('UC', store=True)
    ucdv_r_va = fields.Char(' ', default='-', readonly=True)
    ucdv_r_selection = fields.Selection([
        ('snellen_chart', 'Snellen Chart'),
        ('cambridge_chart', 'Cambridge Chart'),
        ('e_chart', 'E-Chart')
    ], string=' ')
    ucdv_r_pinhole = fields.Char('PH', store=True)
    ucdv_r_cl = fields.Char('CL', store=True)

    ucnv_r_re = fields.Char('PG', store=True, default=' ')
    ucnv_r_le = fields.Char('UC', store=True, default=' ')
    ucnv_r_va = fields.Char(' ', readonly=True, default='-')
    ucnv_r_selection = fields.Selection([
        ('snellen_chart', 'Snellen Chart'),
        ('cambridge_chart', 'Cambridge Chart'),
        ('e_chart', 'E-Chart')
    ], string=' ')
    ucnv_r_pinhole = fields.Char('PH', store=True, default=' ')
    ucnv_r_cl = fields.Char('CL', store=True, default=' ')

    # dilated_ar_ids fields
    #     AR
    dilated_ar_le_ar = fields.Char(' ', default='AR')
    va_le_ar = fields.Char(string='V/A', store=True)
    sphere_le_ar = fields.Char(string='Sph', store=True)
    cyl_le_ar = fields.Char(string='Cyl', store=True)
    axis_le_ar = fields.Char(string='Axis', store=True)
    # color_status = fields.Boolean(default=False)
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
    # RS
    dilated_ar_le_rs = fields.Char(' ', default='RS')
    va_le_rs = fields.Char(string='V/A', store=True)
    sphere_le_rs = fields.Char(string='Sph', store=True)
    cyl_le_rs = fields.Char(string='Cyl', store=True)
    axis_le_rs = fields.Char(string='Axis', store=True)

    # dilated_ar_re_ids fields
    #     AR
    dilated_ar_re_ar = fields.Char(' ', default='AR')
    va_re_ar = fields.Char(string='V/A', store=True)
    sphere_re_ar = fields.Char(string='Sph', store=True)
    cyl_re_ar = fields.Char(string='Cyl', store=True)
    axis_re_ar = fields.Char(string='Axis', store=True)
    # color_status = fields.Boolean(default=False)
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
    # RS
    dilated_ar_re_rs = fields.Char(' ', default='RS')
    va_re_rs = fields.Char(string='V/A', store=True)
    sphere_re_rs = fields.Char(string='Sph', store=True)
    cyl_re_rs = fields.Char(string='Cyl', store=True)
    axis_re_rs = fields.Char(string='Axis', store=True)

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

    procedure_type = fields.Selection([
        ('investigation', 'Investigation Procedure'),
        ('treatment', 'Treatment Procedure')], string='Procedure Type')

    @api.onchange('date')
    def onchange_admission_date(self):
        if self.date:
            date_admission = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S").date()
            date_today = date.today()
            if date_admission < date_today:
                raise UserError('Admission date must be greater than current')

    @api.onchange('referred_by_id')
    def get_reference_by_id(self):
        self.reference_type_id = self.referred_by_id.type_id.id

    @api.depends('birthdate_date')
    def _compute_age(self):
        """ Age computed depending based on the birth date in the
         membership request.
        """
        now = datetime.now()
        for record in self:
            if record.birthdate_date:
                birthdate_date = fields.Datetime.from_string(
                    record.birthdate_date,
                )
                if record.is_deceased:
                    date_death = fields.Datetime.from_string(record.date_death)
                    delta = relativedelta(date_death, birthdate_date)
                    is_deceased = _(' (deceased)')
                else:
                    delta = relativedelta(now, birthdate_date)
                    is_deceased = ''
                years_months_days = '%d%s %d%s %d%s%s' % (
                    delta.years, _('y'), delta.months, _('m'),
                    delta.days, _('d'), is_deceased
                )
                years = delta.years
            else:
                years_months_days = _('No DoB')
                years = False
            record.age = years_months_days
            if years:
                record.age_years = years

    @api.multi
    def _compute_is_deceased(self):
        pass

    @api.multi
    def unlink(self):
        res = super(PatientRevisit, self).unlink()
        if not self.env.user.has_group('base.group_system'):
            raise UserError('You have no access to delete a Visit')
        return res
