from odoo import api, models, fields, _
from datetime import datetime, date
from odoo.exceptions import UserError


class MedicalOptics(models.Model):
    _name = 'medical.optics'
    _description = 'Optics Details'
    _rec_name = 'sequence'
    _order = 'sequence desc'

    @api.model
    def create(self, vals):
        if not vals.get('sequence'):
            if 'patient_id' in vals:
                vals['sequence'] = self.env['ir.sequence'].next_by_code(
                    'medical.optics') or _('New')

        return super(MedicalOptics, self).create(vals)

    def default_journal_id(self):
        journal = self.env['account.journal'].search([('default_journal', '=', True)], limit=1)
        return journal.id

    refraction_id = fields.Many2one('res.users', string="Refractionist")

    name = fields.Char(string='Patient Reference', copy=False, readonly=True, index=True)

    sequence = fields.Char(required=True, copy=False, readonly=True, index=True,
                           ondelete='cascade', default=lambda self: _('New'), )

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True,
                                   help="Pricelist for current sales order.", default=1)

    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True,
                                  required=True)

    patient_id = fields.Many2one('medical.patient', string='Patient Name', required=True)

    new_patient_is = fields.Boolean('New Patient')

    patient_new = fields.Char(string='New Patient')

    phone = fields.Char('Contact Number', related='patient_id.phone', required=True)

    city = fields.Char(related='patient_id.city')

    zip = fields.Char(change_default=True, related='patient_id.zip')

    birthdate_date = fields.Date('Birth Date', related='patient_id.birthdate_date', required=True)

    street = fields.Char(related='patient_id.street')

    street2 = fields.Char(related='patient_id.street2')

    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', related='patient_id.state_id')

    identification_code = fields.Char('File Number', related='patient_id.identification_code', store=True)

    delivery_date = fields.Date('Delivery Date')

    age = fields.Char('Age')

    patient_visit_id = fields.Many2one('medical.opthalmology')

    search_file_number = fields.Char('Search File Number')

    reference_type_id = fields.Many2one('reference.type', 'Reference Type')

    sales_person_id = fields.Many2one('hr.employee', string='Sales Person')

    gender = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ], related='patient_id.gender')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('work_order', 'Work Order'),
        ('done', 'Done')], string='Status',
        default='draft')

    date = fields.Datetime('Admission Date', default=fields.Datetime.now)

    date_today = fields.Date('Date', default=fields.Date.context_today, readonly=True, )

    doctor_id = fields.Many2one('medical.practitioner', string='Doctor')

    glass_prescription = fields.Text('Glass Prescription')

    reject_reason=fields.Many2one('work.order.reject.reason',string="Cancel Reason", track_visibility='onchange',readonly=1)


    def sent_to_done(self):
        view = self.env.ref('medical_opthalmology.work_order_reject_wizard_view')
        return {
            'name': "Cancel Reason",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'work.order.reject.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {
                'default_optics_id': self.id,'default_sales_person_id': self.sales_person_id.id if self.sales_person_id else False,
            },

        }


    @api.model
    def default_dilated_refraction_le_ids(self):
        old_glass_list = ['DV', 'ADD']
        ids = []
        for item in old_glass_list:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    def default_dilated_refraction_ids(self):
        old_glass_list = ['DV', 'ADD']
        ids = []
        for item in old_glass_list:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    dilated_refraction_le_ids = fields.One2many('dilated.refraction.optics', 'patient_visit_id',
                                                default=default_dilated_refraction_le_ids, force_save=True)

    dilated_refraction_ids = fields.One2many('dilated.refraction.optics', 'patient_visit_re_id',
                                             default=default_dilated_refraction_ids)

    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', related='patient_id.country_id')

    tag_ids = fields.Many2many('patient.visit.tag', string='Tags', )

    total_amount = fields.Float('Total Amount', compute='compute_total_optics_amount')

    discount_type = fields.Selection([
        ('amount', 'Fixed'),
        ('percent', 'Percentage')
    ])
    discount = fields.Float('Discount')
    final_total = fields.Float(string='Final Total', compute='compute_final_total_amount')
    advance_amount = fields.Float(string='Advance')
    tax_amount = fields.Float('Tax', compute='_amount_all', store=True)
    journal_id = fields.Many2one('account.journal', string='Payment Type', domain=[('type', 'in', ('cash', 'bank'))],
                                 default=default_journal_id)
    balance_amount = fields.Float(string='Balance Amount', compute='balance_amount_calulation')
    work_order_id = fields.Many2one('optics.work.order', 'Work Order')

    @api.onchange('patient_new')
    def on_change_patient_new(self):
        if self.patient_new:
            patient = self.env['medical.patient'].create({'name': self.patient_new})
            self.patient_id = patient.id

    @api.onchange('phone')
    def _onchange_phone(self):
        if self.phone and not self.new_patient_is and not self.identification_code:

            patient_ids = self.env['medical.patient'].search([('phone', '=', self.phone)])
            if patient_ids:
                patient_id = patient_ids[0]
                self.patient_id = patient_id.id
                self.identification_code = patient_id.identification_code
                self.email = patient_id.email
                self.age = patient_id.patient_age
                self.gender = patient_id.gender
                self.street = patient_id.street
                return {'domain': {'patient_id': [('id', '=', patient_ids.ids)]}}

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.phone = self.patient_id.phone
        self.identification_code = self.patient_id.identification_code
        self.gender = self.patient_id.gender
        self.street = self.patient_id.street
        self.age = self.patient_id.patient_age

    @api.onchange('delivery_date')
    def _onchange_delivery_date(self):
        if self.delivery_date and self.work_order_id:
            self.work_order_id.delivery_date = self.delivery_date

    @api.onchange('search_file_number')
    def _onchange_search_file_number(self):

        new = self.env['medical.patient'].search([('identification_code', '=', self.search_file_number)])
        for i in new:
            if i.identification_code:
                self.patient_id = i.id
                self.phone = i.phone
                self.email = i.email
                self.age = i.patient_age
                self.gender = i.gender
                self.street = i.street

    @api.model
    def default_optics_ids(self):
        ids = []
        for line in range(0, 0):
            data = {
                'product_id': self.product_id.id,
                'quantity': self.quantity,
                'price_unit': self.price_unit,
                'sub_total': self.sub_total,
            }
            ids.append((0, 0, data))
        return ids

    optics_details_ids = fields.One2many('optical.prescription', 'patient_visit_id', string='Optics Details',
                                         default=default_optics_ids)

    @api.depends('optics_details_ids.price_unit', 'optics_details_ids.quantity')
    def compute_total_optics_amount(self):
        for record in self:
            for item in record.optics_details_ids:
                record.total_amount += (item.price_unit) * (item.quantity)

    @api.depends('total_amount', 'discount_type', 'discount', 'tax_amount')
    def compute_final_total_amount(self):
        for record in self:
            if record.total_amount:
                if record.discount:
                    if record.discount_type == 'amount':
                        record.final_total = (record.total_amount - record.discount) + record.tax_amount
                    else:
                        record.final_total = (record.total_amount - (
                                record.total_amount * ((record.discount) / 100))) + record.tax_amount
                else:
                    record.final_total = record.total_amount + record.tax_amount

    @api.depends('final_total', 'advance_amount')
    def balance_amount_calulation(self):
        for rec in self:
            rec.balance_amount = rec.final_total - rec.advance_amount

    @api.onchange('discount_type', 'discount', 'optics_details_ids')
    def supply_rate(self):
        for order in self:
            if order.discount_type == 'percent':
                for line in order.optics_details_ids:
                    line.discount = order.discount
            else:
                total = discount = 0.0
                for line in order.optics_details_ids:
                    total += round((line.quantity * line.price_unit))
                if order.discount != 0:
                    discount = (order.discount / total) * 100
                else:
                    discount = order.discount
                for line in order.optics_details_ids:
                    line.discount = discount

    @api.depends('optics_details_ids.price_total', 'optics_details_ids.tax_ids', 'final_total')
    def _amount_all(self):
        """
        Compute the total amounts of the Prescription.
        """
        for order in self:
            amount_tax = 0.0
            for line in order.optics_details_ids:
                amount_tax += line.price_tax
            order.update({
                'tax_amount': amount_tax,
            })

    def create_work_order(self):
        debit_vals = []
        payment = False
        if not self.delivery_date:
            raise UserError('Please enter Delivery Date')
        for record in self.optics_details_ids:
            vals = {
                'product_id': record.product_id.id,
                'name': record.product_id.name,
                'product_uom_qty': record.quantity,
                'qty_to_invoice': record.quantity,
                'price_unit': record.price_unit,
                'tax_id': [(6, 0, record.tax_ids.ids)]
            }
            debit_vals.append((0, 0, vals))

        record = self.env['optics.work.order'].create(
            {
                'phone': self.phone,
                'identification_code': self.identification_code,
                'partner_id': self.patient_id.partner_id.id,
                'age': self.age,
                'gender': self.gender,
                'doctor_id': self.doctor_id.id,
                'date': self.date,
                'order_line': debit_vals,
                'patient_visit_id': self.id,
                'discount_type': self.discount_type,
                'discount_rate': self.discount,
                'advance_amount': self.advance_amount,
                'refraction_id': self.refraction_id.id,
                # 'balance_amount': self.balance_amount,
                'delivery_date': self.delivery_date,
                'payment_id': payment and payment.id,
                'medical_optics_id': self.id,
                'sales_person_id': self.sales_person_id.id,
            })
        self.work_order_id = record.id,
        record.order_id.supply_rate()
        record.order_id.doctor_id = self.doctor_id.id
        record.order_id.action_confirm()
        record.order_id.action_invoice_create()
        record.order_id.invoice_ids.action_invoice_open()
        for invoice in record.order_id.invoice_ids:
            invoice.optics_bool = True
            invoice.doctor_id = self.doctor_id.id
            invoice.identification_code = self.identification_code
            invoice.sale_order_id = record.order_id.id
        if self.final_total and self.advance_amount:
            payment = self.env['account.payment'].create({
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'invoice_ids': [(6, 0, record.order_id.invoice_ids.ids)],
                'partner_id': self.patient_id.partner_id.id,
                'amount': self.advance_amount,
                'payment_date': self.date,
                'payment_method_id': (
                    self.env['account.payment.method'].search([('payment_type', '=', 'inbound')], limit=1)).id,
                'communication': self.patient_id.name + self.sequence,
                'journal_id': self.journal_id.id,
                'optics_payment_bool': True,

            })
            payment.post()
        self.state = 'work_order'
        self.patient_visit_id.update({
            'state': 'done'
        })

    def print_eye_details(self):

        return self.env.ref('medical_opthalmology.print_eye_detail_template').report_action(self)

    def print_work_order(self):
        return self.env.ref('medical_opthalmology.print_work_order_template').report_action(self)

    @api.multi
    def unlink(self):
        res = super(MedicalOptics, self).unlink()
        raise UserError('You can not delete a Visit')
        return res


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_registraion_product_id = fields.Many2one(
        'product.product',
        'Registration Fee',
        domain="[('type', '=', 'service')]",
        help='Default product used for Registration payments')
