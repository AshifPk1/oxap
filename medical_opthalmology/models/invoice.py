from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    patient_visit_id = fields.Many2one('Medical.opthalmology', 'Patient Visit ID')
    identification_code = fields.Char('File Number', readonly=True, states={'draft': [('readonly', False)]})
    payment_journal_id = fields.Many2one('account.journal', 'Payment Journal')
    registration_bool = fields.Boolean('Registration', default=False)
    surgery_bool = fields.Boolean('surgery', default=False)
    investigation_bool = fields.Boolean('Investigation', default=False)
    procedure_bool = fields.Boolean('Procedure', default=False)
    optics_bool = fields.Boolean('Optics', default=False)
    pharmacy_bool = fields.Boolean('Pharmacy', default=False)

    def _get_refund_common_fields(self):
        return super(AccountInvoice, self)._get_refund_common_fields() + ['pharmacy_bool', 'optics_bool',
                                                                          'investigation_bool', 'surgery_bool',
                                                                          'registration_bool', 'procedure_bool']

    @api.onchange('identification_code')
    def _onchange_identification_code(self):

        patient_id = self.env['medical.patient'].search([('identification_code', '=', self.identification_code)])
        for i in patient_id:
            if i.identification_code:
                self.partner_id = i.partner_id.id


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def default_journal_id(self):
        record = self.env['account.journal'].search([('default_journal', '=', True)], limit=1)
        return record.id

    signed_total = fields.Float('Collection Amount', compute='payment_amount_sign_compute', store=True)
    journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True, default=default_journal_id,
                                 domain=[('type', 'in', ('bank', 'cash'))])

    @api.depends('payment_type')
    def payment_amount_sign_compute(self):
        for record in self:
            if record.payment_type == 'outbound':
                record.signed_total = -record.amount
            elif record.payment_type == 'inbound':
                record.signed_total = record.amount

    @api.multi
    def action_validate_invoice_payment(self):
        res = super(AccountPayment, self).action_validate_invoice_payment()
        for record in self.invoice_ids:
            if record.registration_bool:
                self.registration_payment_bool = True
            if record.surgery_bool:
                self.surgery_payment_bool = True
            if record.investigation_bool:
                self.investigation_payment_bool = True
            if record.optics_bool:
                self.optics_payment_bool = True
            if record.pharmacy_bool:
                self.pharmacy_payment_bool = True
            if record.procedure_bool:
                self.procedure_payment_bool = True
            if record.residual == 0:
                record.sale_order_id.write({'state': 'paid'})
        return res

    registration_payment_bool = fields.Boolean('Registration', default=False)
    surgery_payment_bool = fields.Boolean('surgery', default=False)
    investigation_payment_bool = fields.Boolean('Investigation', default=False)
    optics_payment_bool = fields.Boolean('Optics', default=False)
    pharmacy_payment_bool = fields.Boolean('Pharmacy', default=False)
    procedure_payment_bool = fields.Boolean('Procedure', default=False)


class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    @api.multi
    def invoice_refund(self):
        res = super(AccountInvoiceRefund, self).invoice_refund()
        return res
