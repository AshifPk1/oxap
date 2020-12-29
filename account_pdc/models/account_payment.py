from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import datetime, date, timedelta


class AccountRegisterPayments(models.TransientModel):
    _inherit = "account.register.payments"

    bank_reference = fields.Char(copy=False)
    cheque_reference = fields.Char(copy=False)
    effective_date = fields.Date('Effective Date', help='Effective date of PDC', copy=False, default=False)

    def get_payment_vals(self):
        res = super(AccountRegisterPayments, self).get_payment_vals()
        if self.payment_method_id == self.env.ref('account_check_printing.account_payment_method_check'):
            res.update({
                'check_amount_in_words': self.check_amount_in_words,
                'check_manual_sequencing': self.check_manual_sequencing,
                'effective_date': self.effective_date,
            })
        return res

    @api.multi
    def process_pdc(self):
        Payment = self.env['account.payment']
        payments_pdc = self.env['account.payment'].search(
            [('invoice_ids', '=', self.invoice_ids.ids), ('state', '=', 'pdc')], limit=1)
        if payments_pdc:
            raise UserError(_("Payment for the selected invoices already exist in PDC state "))

        else:
            payments = Payment
            for payment_vals in self.get_payments_vals():
                payments += Payment.create(payment_vals)
            for payment in payments:
                payment.update({'state': 'pdc',
                                'effective_date': self.effective_date})
            return {
                'name': _('Payments'),
                'domain': [('id', 'in', payments.ids), ('state', '=', 'pdc')],
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.payment',
                'view_id': False,
                'type': 'ir.actions.act_window',
            }

    @api.multi
    def _prepare_payment_vals(self, invoices):
        res = super(AccountRegisterPayments, self)._prepare_payment_vals(invoices)
        print(res, 'res')

        return res

class AccountPayment(models.Model):
    _inherit = "account.payment"

    bank_reference = fields.Char(copy=False)
    cheque_reference = fields.Char(copy=False)
    effective_date = fields.Date('Effective Date', help='Effective date of PDC', copy=False, default=False)
    state = fields.Selection(selection_add=[('pdc', 'PDC'), ], )
    check_effective_date = fields.Boolean(compute='_compute_check_date')

    @api.depends('effective_date')
    def _compute_check_date(self):
        for rec in self:
            if rec.effective_date:
                if rec.effective_date < str(date.today()):
                    rec.check_effective_date = True
                else:
                    rec.check_effective_date = False

    @api.multi
    def print_checks(self):
        """ Check that the recordset is valid, set the payments state to sent and call print_checks() """
        # Since this method can be called via a client_action_multi, we need to make sure the received records are what we expect
        self = self.filtered(
            lambda r: r.payment_method_id.code in ['check_printing', 'pdc'] and r.state != 'reconciled')

        if len(self) == 0:
            raise UserError(_("Payments to print as a checks must have 'Check' or 'PDC' selected as payment method and "
                              "not have already been reconciled"))
        if any(payment.journal_id != self[0].journal_id for payment in self):
            raise UserError(_("In order to print multiple checks at once, they must belong to the same bank journal."))

        if not self[0].journal_id.check_manual_sequencing:
            # The wizard asks for the number printed on the first pre-printed check
            # so payments are attributed the number of the check the'll be printed on.
            last_printed_check = self.search([
                ('journal_id', '=', self[0].journal_id.id),
                ('check_number', '!=', 0)], order="check_number desc", limit=1)
            next_check_number = last_printed_check and last_printed_check.check_number + 1 or 1
            return {
                'name': _('Print Pre-numbered Checks'),
                'type': 'ir.actions.act_window',
                'res_model': 'print.prenumbered.checks',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'payment_ids': self.ids,
                    'default_next_check_number': next_check_number,
                }
            }
        else:
            self.filtered(lambda r: r.state == 'draft').post()
            self.write({'state': 'sent'})
            return self.do_print_checks()

    def _get_move_vals(self, journal=None):
        """ Return dict to create the payment move
        """
        journal = journal or self.journal_id
        if not journal.sequence_id:
            raise UserError(_('Configuration Error !'),
                            _('The journal %s does not have a sequence, please specify one.') % journal.name)
        if not journal.sequence_id.active:
            raise UserError(_('Configuration Error !'), _('The sequence of journal %s is deactivated.') % journal.name)
        name = self.move_name or journal.with_context(ir_sequence_date=self.payment_date).sequence_id.next_by_id()
        if self.payment_method_code == 'pdc':
            date = self.effective_date
        else:
            date = self.payment_date
        return {
            'name': name,
            'date': date,
            'ref': self.communication or '',
            'company_id': self.company_id.id,
            'journal_id': journal.id,
        }

    # payment_method_code

    @api.multi
    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconciliable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:

            # if rec.state not in ['draft','pdc']:
            #     raise UserError(_("Only  draft or pdc payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(
                    sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(
                    lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                # persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
        return True

    @api.one
    def process_pdc(self):
        self.write({
            'state': 'pdc',
        })
