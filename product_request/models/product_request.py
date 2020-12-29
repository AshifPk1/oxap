
from odoo import models, fields, api,_


class ProductRequest(models.Model):
    _name = "product.request"
    _description = "Product Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Service Number", readonly=True, required=True, copy=False, default='New')

    request_date = fields.Date("Request Date", track_visibilty="always")
    doctor = fields.Many2one('medical.practitioner', "Doctor", track_visibilty="always")
    user = fields.Many2one('res.users', 'Requested By', default=lambda self: self.env.user, track_visibilty="always")
    product_ids = fields.One2many('product.request.line', 'request_id', string='Products')
    state = fields.Selection([('draft', 'Draft'), ('requested', 'Requested'),
                              ('approved', 'Approved'), ('done', 'Done'), ('cancelled', 'Cancelled')], 'State',
                             default='draft')
    request_ids = fields.One2many('purchase.order', 'product_request_id', string="request ids")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'product.request.sequence') or 'New'
        result = super(ProductRequest, self).create(vals)
        return result

    @api.multi
    def open_rfq(self):
        return {
            'name': _('RFQ'),
            'domain': [('product_request_id', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': {'default_product_request_id': self.id}
        }

    def action_requested(self):
        self.state = 'requested'

    def action_approved(self):
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_done(self):
        self.state = 'done'


class ProductRequestLines(models.Model):
    _name = 'product.request.line'
    request_id = fields.Many2one('product.request', string="Request")
    product_name = fields.Char("Product Name")
    generic_name = fields.Char("Generic Name")
    qty_req = fields.Float("Required Quantity")
    brand = fields.Char("Brand")


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"
    product_request_id = fields.Many2one('product.request', string="Request ID")
