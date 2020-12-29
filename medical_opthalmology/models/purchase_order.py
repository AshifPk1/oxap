from datetime import date
from odoo import models, fields


class purchase_order(models.Model):
    _inherit = "purchase.order"

    date_today = fields.Date('Date', default=date.today(), readonly=True, )
    is_frame_purchase = fields.Boolean(default=False)
    is_lense_purchase = fields.Boolean(default=False)
    is_surgicallense_purchase = fields.Boolean(default=False)
    is_pharmacy_purchase = fields.Boolean(default=False)
