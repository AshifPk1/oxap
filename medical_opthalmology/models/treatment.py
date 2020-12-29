from odoo import api, models, fields


class OpticalTreatmnet(models.Model):
    _inherit = 'medical.opthalmology'

    @api.model
    def default_treatment_id(self):
        ids = []
        for line in range(0, 0):
            data = {
                'patient_visit_id': self.id,
            }
            ids.append((0, 0, data))
        return ids

    treatment_ids = fields.One2many('optical.treatment', 'patient_visit_id', string='Treatment Details',
                                    ondelete='cascade', default=default_treatment_id)
    medicine_ids = fields.One2many('doctor.treatment', 'medicine_id', string='Medications')


class DoctorTreatment(models.Model):
    _name = 'doctor.treatment'

    medicine_id = fields.Many2one('medical.opthalmology')
    pharmacy_id = fields.Many2one('medical.pharmacy')
    product_id = fields.Many2one('product.template', string='Product', domain=[('is_pharmacy', '=', True)],
                                 required=True)
    categ_id = fields.Many2one('product.category', string='Product Category', related='product_id.categ_id',readonly=True)

    days = fields.Char(string='Days')
    frequency = fields.Char(string='Frequency')
    frequency_id = fields.Many2one('pharmacy.frequency', string='Frequency')
    stock = fields.Float(string='Stock', compute='view_stock_qty', store=True)
    eye = fields.Selection([('left_eye', 'LE'), ('right_eye', 'RE'), ('both', 'BE')], string='Eye')

    @api.depends('product_id')
    def view_stock_qty(self):
        for rec in self:
            rec.stock = rec.product_id.qty_available


class PharmacyFrequency(models.Model):
    _name = 'pharmacy.frequency'

    name = fields.Char(string='Frequency')
