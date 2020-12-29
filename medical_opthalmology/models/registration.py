from datetime import datetime, date
from odoo import api, models, fields, _
from odoo.api import Environment
from odoo.exceptions import UserError


class PatientRegistration(models.Model):
    _inherit = 'medical.opthalmology'

    def default_journal_id(self):
        journal = self.env['account.journal'].search([('default_journal', '=', True)], limit=1)
        return journal.id

    tag_ids = fields.Many2many('patient.visit.tag', string='Tags', )
    waiting_time = fields.Char(compute='compute_waiting_time', string='Waiting Time', readonly=True)
    sequence = fields.Char()
    product_id = fields.Many2one('product.product', 'Registration Fee')
    last_payment_date = fields.Date('Last Payment Date', readonly=True)
    last_payment_days = fields.Char('Last payment in Days', readonly=True)
    registration_amount = fields.Monetary('Registration Fee')
    journal_id = fields.Many2one('account.journal', 'Payment Method', domain="[('type', 'in', ['cash','bank'])]",
                                 default=default_journal_id)
    search_file_number = fields.Char('Search File Number')
    is_refund = fields.Boolean(string='Refund')

    age_in_float = fields.Float(string="Float Age", compute="_age_float", store=True)

    @api.depends('age')
    def _age_float(self):
        for rec in self:
            if rec.age:
                string = rec.age
                float_value = ''
                age = 0
                try:
                    float(string)
                    res = True
                except:
                    res = False
                if not res:
                    for i in string:
                        if i.isdigit() or i == '.':
                            float_value = float_value + i
                    if float_value:
                        try:
                            float_value = float(float_value)
                        except:
                            break
                        if 'd' in string or 'D' in string:
                            age = float_value / 30
                            age = age / 12
                        elif 'm' in string or 'M' in string:
                            age = float_value / 12

                        elif 'Y' in string or 'y' in string:
                            age = float_value
                        else:
                            age = float_value
                    rec.age_in_float = age
                else:
                    rec.age_in_float = float(string)

    @api.multi
    def action_invoice_cancel(self):
        description = 'refund'
        date = fields.Date.today() or False
        refund = False
        if self.registartion_invoice_id:
            invoices = self.registartion_invoice_id
            for inv in invoices:
                description = description or inv.name
                try:
                    refund = inv.refund(date, date, description, inv.journal_id.id)
                except:
                    raise UserError(('Credit Note Already Created'))
            if refund:
                for invoice in refund:
                    invoice.registration_bool = True
                    self.is_refund = True
                    return self.registerpayment(invoice)

    @api.multi
    def registerpayment(self, invoice):
        invoice.action_invoice_open()
        view = self.env.ref('account.view_account_payment_invoice_form')
        context = self.env.context.copy()
        context['default_invoice_ids'] = [(6, 0, [invoice.id])]
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

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'patient_id' in vals:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'medical.opthalmology') or _('New')
                vals['sequence'] = vals['name']
                vals['new_details'] = True
        return super(PatientRegistration, self).create(vals)

    @api.multi
    def new_patient(self):
        view = self.env.ref('medical.medical_patient_view_form')
        return {
            'name': _('New Patient'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'medical.patient',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
        }

    @api.depends('date')
    def compute_waiting_time(self):
        new = self.env['medical.opthalmology'].search([('state', '=', 'waiting')])
        for record in new:
            if record.date:
                admission_date = datetime.strptime(record.date, "%Y-%m-%d %H:%M:%S")
                date_now = str(datetime.now().replace(microsecond=0))
                current_time = datetime.strptime(date_now, "%Y-%m-%d %H:%M:%S")
                record.waiting_time = current_time - admission_date

    def confirm_registration_warning(self):
        view = self.env.ref('medical_opthalmology.registration_warning_wizard_view')
        context = self.env.context.copy()

        return {
            'name': _('Warning'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'registration.warning.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {
                'default_patient_id': self.patient_id.id,
                'default_doctor_id': self.doctor_id.id,
                'default_identification_code': self.identification_code,
                'default_registration_amount': self.registration_amount,
                'default_last_payment_date': self.last_payment_date,
                'default_journal_id': self.journal_id.id,
                'default_phone': self.phone,
            },
        }

    @api.multi
    def confirm(self):

        if self.phone:
            # registration SMS
            record = self.env['gateway_setup'].search([], limit=1)
            record.update(
                {
                    'mobile': self.phone,
                    'message': 'Thank you %s .\nYour registration has been succesfully done for the %s \nFile Number: %s \nAdmission Date: %s' % (
                        self.patient_id.name, self.doctor_id.name, self.identification_code, self.date_today)
                }
            )
            try:
                record.sms_test_action()
            except:
                pass

        if self.registration_amount > 0 and self.journal_id:
            if self.move_state:
                self.state = self.move_state
            if self.state == 'registration':
                self.write({'state': 'waiting'})
            if self.state == 'surgery':
                self.write({'surgery_date': date.today()})

            env_thread1 = Environment(self._cr, self._uid, self._context)
            product = self.env['product.product'].search([('is_registration_product', '=', True)], limit=1)
            if not product:
                raise UserError(
                    _('Please define a Registration Product'))
            invoice_obj = self.env['account.invoice']
            account_payment_obj = env_thread1['account.payment']
            if self.counselling_invoice_id:
                context = self.env.context.copy()

                return {
                    'name': _('Invoice'),
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'account.invoice',
                    'target': 'new',
                    'context': context,
                    'res_id': self.counselling_invoice_id.id,
                }
            else:
                account = product.property_account_income_id or product.categ_id.property_account_income_categ_id
                if not account:
                    raise UserError(
                        _('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                        (product.name, product.id, product.categ_id.name))

                vals = {
                    'name': product.name,
                    'quantity': 1,
                    'uom_id': 1,
                    'account_id': account.id,
                    'product_id': product.id,
                    'price_unit': self.registration_amount,

                }
                # TDE FIXME: what is default values(account_id,product, ??
                record = invoice_obj.create({
                    # 'payment_journal_id': self.journal_id.id,
                    'partner_id': self.patient_id.partner_id.id,
                    'identification_code': self.patient_id.identification_code,
                    'doctor_id': self.doctor_id.id,
                    'date_invoice': self.date,
                    'invoice_line_ids': [(0, 0, vals)],
                    'patient_visit_id': self.id,
                    'registration_bool': True,
                })

                self.registartion_invoice_id = record.id
                record.action_invoice_open()

                vals = {
                    'journal_id': self.journal_id.id,
                    'invoice_ids': [(6, 0, [record.id])],
                    'communication': record.reference,
                    'currency_id': record.currency_id.id,
                    'payment_type': 'inbound',
                    'partner_id': record.commercial_partner_id.id,
                    'amount': record.residual,
                    'payment_method_id': self.journal_id.inbound_payment_method_ids.id,
                    'partner_type': 'customer',
                    'registration_payment_bool': True,

                }
                new_rec = account_payment_obj.create(vals)
                new_rec.post()
        else:
            if self.move_state:
                self.state = self.move_state
            if self.state == 'registration':
                self.write({'state': 'waiting'})
            if self.state == 'surgery':
                self.write({'surgery_date': date.today()})

    @api.multi
    def print_invoice(self):
        return self.env.ref('medical_opthalmology.action_report_registration_invoice').report_action(self)

    @api.multi
    def print_slip(self):
        return self.env.ref('medical_opthalmology.action_report_registration_slip').report_action(self)
