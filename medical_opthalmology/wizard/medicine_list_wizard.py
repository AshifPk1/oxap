from odoo import models, api, fields


class medicineListwizard(models.TransientModel):
    _name = 'medicine.list.wizard'

    parent_id = fields.Many2one('medical.opthalmology', string='Parent', readonly=1)
    medicine_line_ids = fields.One2many('medicine.list.line.wizard', 'medicine_id', readonly=1, string='Medications')

    def update_medicine(self):
        record = self.env['medical.opthalmology'].search([('id', '=', self.parent_id.id)])
        ids = []
        for line in self.medicine_line_ids:
            data = dict(product_id=line.product_id.id, days=line.days, eye=line.eye, stock=line.stock,
                        frequency_id=line.frequency_id.id)
            ids.append(data)

        record.update(
            {
                'medicine_ids': [(0, 0, id) for id in ids]

            }
        )


class medicineListLinewizard(models.TransientModel):
    _name = 'medicine.list.line.wizard'

    medicine_id = fields.Many2one('medicine.list.wizard', readonly=1, string='Medications')

    product_id = fields.Many2one('product.template', required=True, string='Product',
                                 domain=[('is_pharmacy', '=', True)])
    days = fields.Char(string='Days')
    frequency = fields.Char(string='Frequency')
    frequency_id = fields.Many2one('pharmacy.frequency', string='Frequency')
    stock = fields.Float(string='Stock', store=True)
    eye = fields.Selection([('left_eye', 'LE'), ('right_eye', 'RE'), ('both', 'BE')], string='Eye')
