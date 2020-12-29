from odoo import models, fields


class Product(models.Model):
    _inherit = 'product.template'

    is_surgery_package = fields.Boolean('Surgery Packages')
    is_investigations = fields.Boolean('Investigations')
    is_procedure = fields.Boolean('Procedure')
    is_surgery_lens = fields.Boolean('Surgery Lens')
    is_lens = fields.Boolean('Lens')
    is_frame = fields.Boolean('Frames')
    is_pharmacy = fields.Boolean('Pharmacy')
    is_registration_product = fields.Boolean(default=False, string='Registration Product')
    power = fields.Char('Power')
    item = fields.Char('Item')
    rate = fields.Float('Amount')
