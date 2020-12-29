from odoo import models, fields


class WorkOrderRejectReason(models.Model):
    _name = "work.order.reject.reason"

    name=fields.Char(String="Name")
