from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class WorkOrder(models.Model):
    _name = 'pharmacy.work.order'
    _rec_name = 'order_id'
    _order = 'id'

    order_id = fields.Many2one('sale.order', 'Order', delegate=True,
                               required=True, ondelete='cascade')

    optics_invoice_id = fields.Many2one('account.invoice', 'Invoice',
                                        copy=False)

    phone = fields.Char('Contact Number', required=True, ondelete='cascade', )

    identification_code = fields.Char('File Number', ondelete='cascade', )

    age = fields.Char('Age', ondelete='cascade', )

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], ondelete='cascade')

    state = fields.Selection(related='order_id.state')

    date = fields.Datetime('Admission Date', default=fields.Datetime.now, readonly=True, ondelete='cascade')

    doctor_id = fields.Many2one('medical.practitioner', string='Doctor', ondelete='cascade')

    work_order_line = fields.One2many('optics.work.order.line', 'work_order_id')

    patient_visit_id = fields.Many2one('medical.pharmacy')

    @api.multi
    def action_view_sale_advance_payment_inv(self):
        view = self.env.ref('sale.view_sale_advance_payment_inv')
        context = self.env.context.copy()
        context['active_ids'] = [self.order_id.id]
        context['active_id'] = self.order_id.id
        return {
            'name': _('Invoice?'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.advance.payment.inv',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def print_invoice(self):
        if self.order_id.invoice_ids.state == 'open' or self.order_id.invoice_ids.state == 'paid':
            record = self.env['account.invoice'].search([('id', '=', (self.order_id.invoice_ids.ids)[0])])
            return record.invoice_print()

    @api.multi
    def registerpayment(self):
        self.order_id.invoice_ids.action_invoice_open()
        view = self.env.ref('account.view_account_payment_invoice_form')
        context = self.env.context.copy()
        context['default_invoice_ids'] = [(6, 0, self.order_id.invoice_ids.ids)]
        return {
            'name': _('Payment?'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
            'pharmacy_bool': True,
        }

    @api.multi
    def action_cancel_draft(self):

        if not len(self._ids):
            return False
        query = "select id from sale_order_line \
            where order_id IN %s and state=%s"
        self._cr.execute(query, (tuple(self._ids), 'cancel'))
        cr1 = self._cr
        line_ids = map(lambda x: x[0], cr1.fetchall())
        self.write({'state': 'draft', 'invoice_ids': []})
        sale_line_obj = self.env['sale.order.line'].browse(line_ids)
        sale_line_obj.write({'invoiced': False, 'state': 'draft',
                             'invoice_lines': [(6, 0, [])]})
        return True

    @api.multi
    def action_confirm(self):
        self.order_id.action_confirm()

    @api.multi
    def action_cancel(self):

        if not self.order_id:
            raise ValidationError(_('Order id is not available'))
        for sale in self:
            for invoice in sale.invoice_ids:
                invoice.state = 'cancel'
        return self.order_id.action_cancel()


class WorkOrderLine(models.Model):
    _name = 'optics.work.order.line'

    work_order_line = fields.Many2one('sale.order.line', 'Order Line', delegate=True,
                                      required=True, ondelete='cascade')

    work_order_id = fields.Many2one('optics.work.order')

    @api.onchange('product_id')
    def product_id_change(self):

        if self.product_id and self.work_order_id.partner_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.list_price
            self.product_uom = self.product_id.uom_id
            tax_obj = self.env['account.tax']
            prod = self.product_id
            self.price_unit = tax_obj._fix_tax_included_price(prod.price,
                                                              prod.taxes_id,
                                                              self.tax_id)

    @api.onchange('product_uom')
    def product_uom_change(self):

        if not self.product_uom:
            self.price_unit = 0.0
            return
        self.price_unit = self.product_id.list_price
        if self.work_order_id.partner_id:
            prod = self.product_id.with_context(
                lang=self.work_order_id.partner_id.lang,
                partner=self.work_order_id.partner_id.id,
                quantity=1,
                pricelist=self.work_order_id.pricelist_id.id,
                uom=self.product_uom.id
            )
            tax_obj = self.env['account.tax']
            self.price_unit = tax_obj._fix_tax_included_price(prod.price,
                                                              prod.taxes_id,
                                                              self.tax_id)
