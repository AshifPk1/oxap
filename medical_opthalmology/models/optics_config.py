from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_registraion_product_id = fields.Many2one(
        'product.product',
        'Registration Fee',
        domain="[('type', '=', 'service')]",
        help='Default product used for Registration payments')
