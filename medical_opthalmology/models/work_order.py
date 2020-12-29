from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class WorkOrder(models.Model):
    _name = 'optics.work.order'
    _rec_name = 'order_id'
    _order = 'name desc'

    order_id = fields.Many2one('sale.order', 'Order', delegate=True,
                               required=True, ondelete='cascade')

    optics_invoice_id = fields.Many2one('account.invoice', 'Invoice',
                                        copy=False)

    phone = fields.Char('Contact Number', required=True, ondelete='cascade', )

    identification_code = fields.Char('File Number', ondelete='cascade', )
    medical_optics_id = fields.Many2one('medical.optics', string='Prescription')

    age = fields.Char('Age', ondelete='cascade', )

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], ondelete='cascade')

    state = fields.Selection(related='order_id.state')

    delivery_status = fields.Selection(related='order_id.delivery_status', string="Delivery Status")

    date = fields.Datetime('Admission Date', default=fields.Datetime.now, readonly=True, ondelete='cascade')

    doctor_id = fields.Many2one('medical.practitioner', string='Doctor', ondelete='cascade')

    # work_order_line=fields.One2many('optics.work.order.line','work_order_id')

    patient_visit_id = fields.Many2one('medical.ophthalmology')

    advance_amount = fields.Float(string='Advance')

    balance_amount = fields.Float(string='Balance Amount', compute='compute_balance_amount_optics')

    residual = fields.Float(compute='compute_residual_amount', string='Balance')
    delivery_date = fields.Date('Delivery Date')

    invoice_date = fields.Date('Invoice Date', compute='compute_invoice_date')

    @api.depends('state')
    def compute_balance_amount_optics(self):
        for rec in self:
            if rec.medical_optics_id and rec.medical_optics_id.balance_amount:
                if rec.state != 'paid':
                    rec.balance_amount = rec.medical_optics_id.balance_amount
                else:
                    rec.balance_amount = 0

    @api.depends('order_id.invoice_ids')
    def compute_invoice_date(self):
        for rec in self:
            for line in rec.order_id.invoice_ids:
                rec.invoice_date = line.date_invoice

    @api.multi
    def create_invoice(self):
        invoices = self.order_id.action_invoice_create()
        for invoice in self.order_id.invoice_ids:
            invoice.optics_bool = True
            invoice.sale_order_id = self.order_id.id

    def print_invoice(self):
        for invoice in self.order_id.invoice_ids:
            if invoice.state == 'open' or invoice.state == 'paid':
                return invoice.invoice_print()

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
            for invoice in sale.order_id.invoice_ids:
                invoice.state = 'cancel'
        return self.order_id.action_cancel()

    @api.multi
    def credit_note_optics(self):

        view = self.env.ref('account.view_account_invoice_refund')
        return {
            'name': _('Credit Notes'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.refund',
            'views': [(view.id, 'form')],
            'view_id': False,
            'target': 'new',
            'context': {'active_ids': self.order_id.invoice_ids.ids, 'default_journal_id': 1, 'type': 'out_refund',
                        'default_type': 'out_refund', 'default_partner_id': self.partner_id.id,
                        'default_journal_type': 'sale'},
            'domain': [('type', '=', 'out_refund')],

        }

    @api.depends('order_id.invoice_ids.residual', 'order_id.invoice_ids.move_id',
                 'order_id.invoice_ids.payments_widget')
    def compute_residual_amount(self):
        for record in self:
            if record.order_id.invoice_ids:
                for item in record.order_id.invoice_ids:
                    if item.partner_id.id == record.partner_id.id:
                        record.residual = item.residual
                        if item.state == 'paid':
                            record.order_id.update({'state': 'paid'})
                            record.medical_optics_id.write({'state': 'done'})

    @api.multi
    def delivery_button(self):
        return self.order_id.action_view_delivery()

    @api.multi
    def write(self, vals):
        res = super(WorkOrder, self).write(vals)
        if vals.get('state') == 'paid':
            self.medical_optics_id.write({'state': 'done'})
        return res
