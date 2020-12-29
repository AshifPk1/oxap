from odoo import models, fields


class OldGlassWizard(models.Model):
    _name = 'old.glass.wizard'

    name = fields.Char(string='Patient Reference', required=True, copy=False, readonly=True, index=True,
                       ondelete='cascade')

    patient_id = fields.Many2one('medical.patient', string='Patient Name', required=True, ondelete='cascade',
                                 readonly=True)
    identification_code = fields.Char('File Number', required=True, readonly=True, ondelete='cascade', )

    age = fields.Char('Age', ondelete='cascade', readonly=True, )

    date = fields.Datetime('Admission Date', default=fields.Datetime.now, readonly=True, ondelete='cascade', )

    old_glass_ids = fields.One2many('old.glass', 'old_glass_wizard_id', string='Old Glasses')

    patient_visit_id = fields.Many2one('medical.opthalmology')

    # DV
    dilated_ar_le_dv = fields.Char(' ', default='DV', readonly=True)
    va_le_dv = fields.Char(string='V/A', store=True, readonly=True)
    sphere_le_dv = fields.Char(string='Sph', store=True, readonly=True)
    cyl_le_dv = fields.Char(string='Cyl', store=True, readonly=True)
    axis_le_dv = fields.Char(string='Axis', store=True, readonly=True)
    # NV
    dilated_ar_le_nv = fields.Char(' ', default='ADD', readonly=True)
    va_le_nv = fields.Char(string='V/A', store=True, readonly=True)
    sphere_le_nv = fields.Char(string='Sph', store=True, readonly=True)
    cyl_le_nv = fields.Char(string='Cyl', store=True, readonly=True)
    axis_le_nv = fields.Char(string='Axis', store=True, readonly=True)

    # DV
    dilated_ar_re_dv = fields.Char(' ', default='DV', readonly=True)
    va_re_dv = fields.Char(string='V/A', store=True, readonly=True)
    sphere_re_dv = fields.Char(string='Sph', store=True, readonly=True)
    cyl_re_dv = fields.Char(string='Cyl', store=True, readonly=True)
    axis_re_dv = fields.Char(string='Axis', store=True, readonly=True)
    # NV
    dilated_ar_re_nv = fields.Char(' ', default='ADD', readonly=True)
    va_re_nv = fields.Char(string='V/A', store=True, readonly=True)
    sphere_re_nv = fields.Char(string='Sph', store=True, readonly=True)
    cyl_re_nv = fields.Char(string='Cyl', store=True, readonly=True)
    axis_re_nv = fields.Char(string='Axis', store=True, readonly=True)

    head_re1 = fields.Char(' ', ondelete='cascade', store=True)
    sph_dv_re1 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_dv_re1 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_dv_re1 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_dv_re1 = fields.Char('VA', ondelete='cascade', store=True)

    sph_nv_re1 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_nv_re1 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_nv_re1 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_nv_re1 = fields.Char('VA', ondelete='cascade', store=True)

    head_le1 = fields.Char(' ', ondelete='cascade', store=True)
    sph_dv_le1 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_dv_le1 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_dv_le1 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_dv_le1 = fields.Char('VA', ondelete='cascade', store=True)

    sph_nv_le1 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_nv_le1 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_nv_le1 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_nv_le1 = fields.Char('VA', ondelete='cascade', store=True)

    old_glass1_date = fields.Date('Date')
    old_glass2_date = fields.Date('Date')
    old_glass3_date = fields.Date('Date')

    glass_status1 = fields.Selection([
        ('available', 'Available'),
        ('previous', 'Previous')])

    glass_type1 = fields.Selection([
        ('bi_focal', 'Bifocal'),
        ('uni_focal', 'Unifocal'),
        ('progressive', 'Progressive'), ])

    head_re2 = fields.Char(' ', ondelete='cascade', store=True)
    sph_dv_re2 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_dv_re2 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_dv_re2 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_dv_re2 = fields.Char('VA', ondelete='cascade', store=True)

    sph_nv_re2 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_nv_re2 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_nv_re2 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_nv_re2 = fields.Char('VA', ondelete='cascade', store=True)

    head_le2 = fields.Char(' ', ondelete='cascade', store=True)
    sph_dv_le2 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_dv_le2 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_dv_le2 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_dv_le2 = fields.Char('VA', ondelete='cascade', store=True)

    sph_nv_le2 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_nv_le2 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_nv_le2 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_nv_le2 = fields.Char('VA', ondelete='cascade', store=True)

    glass_status2 = fields.Selection([
        ('available', 'Available'),
        ('previous', 'Previous')])

    glass_type2 = fields.Selection([
        ('bi_focal', 'Bifocal'),
        ('uni_focal', 'Unifocal'),
        ('progressive', 'Progressive'), ])

    head_re3 = fields.Char(' ', ondelete='cascade', store=True)
    sph_dv_re3 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_dv_re3 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_dv_re3 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_dv_re3 = fields.Char('VA', ondelete='cascade', store=True)

    sph_nv_re3 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_nv_re3 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_nv_re3 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_nv_re3 = fields.Char('VA', ondelete='cascade', store=True)

    head_le3 = fields.Char(' ', ondelete='cascade', store=True)
    sph_dv_le3 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_dv_le3 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_dv_le3 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_dv_le3 = fields.Char('VA', ondelete='cascade', store=True)

    sph_nv_le3 = fields.Char('SPH', ondelete='cascade', store=True)
    cyl_nv_le3 = fields.Char('CYL', ondelete='cascade', store=True)
    axis_nv_le3 = fields.Char('AXIS', ondelete='cascade', store=True)
    va_nv_le3 = fields.Char('VA', ondelete='cascade', store=True)

    glass_status3 = fields.Selection([
        ('available', 'Available'),
        ('previous', 'Previous')])

    glass_type3 = fields.Selection([
        ('bi_focal', 'Bifocal'),
        ('uni_focal', 'Unifocal'),
        ('progressive', 'Progressive'), ])
