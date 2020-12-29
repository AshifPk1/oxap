from odoo import api, models, fields, _
from odoo.exceptions import UserError


class Procedure(models.Model):
    _inherit = 'medical.opthalmology'

    procedure_details_ids = fields.One2many('optical.procedure', 'patient_visit_id', string='Procedure')
    sent_to_procedure = fields.Boolean(default=False)

    total_amount_procedure = fields.Float(compute='compute_total_procedure_amount', string='Total Amount')
    discount_type_procedure = fields.Selection([
        ('amount', 'Fixed'),
        ('percent', 'Percentage')
    ])
    discount_procedure = fields.Float('Discount')
    tax_amount_procedure = fields.Float('Tax', compute='_amount_all_procedure', store=True)
    final_total_procedure = fields.Monetary(compute='compute_final_total_amount_procedure', string='Final Total')

    procedure_invoice_id = fields.Many2one('account.invoice')

    invoiced_procedure = fields.Boolean('Procedure Invoiced', default=False)

    procedure_done = fields.Boolean('Procedure Done', default=False)
    procedure_done_by = fields.Char('Procedure Done By')
    description = fields.Text('Description')
    procedure_invoice_status = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ],string='Invoice Status',default='draft',compute='compute_invoice_status')

    @api.onchange('discount_type_procedure', 'discount_procedure', 'procedure_details_ids')
    def supply_rate_procedure(self):
        for order in self:
            if order.discount_type_procedure == 'percent':
                for line in order.procedure_details_ids:
                    line.discount = order.discount_procedure
            else:
                total = discount = 0.0
                for line in order.procedure_details_ids:
                    total += round((line.qty * line.amount))
                if order.discount_procedure != 0:
                    discount = (order.discount_procedure / total) * 100
                else:
                    discount = order.discount_procedure
                for line in order.procedure_details_ids:
                    line.discount = discount

    @api.multi
    def create_order_procedure(self):
        debit_vals = []
        invoice_obj = self.env['account.invoice'].sudo()
        if not self.procedure_invoice_id:
            for record in self.procedure_details_ids:
                account = record.procedure.property_account_income_id or \
                          record.procedure.categ_id.property_account_income_categ_id
                if not account:
                    raise UserError(
                        _('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                        (record.procedure.name, record.procedure.id, record.procedure.categ_id.name))


                vals = {
                    'name': record.procedure.name,
                    'quantity': record.qty,
                    'uom_id': 1,
                    'product_id': record.procedure.id,
                    'account_id': account.id,
                    'price_unit': record.amount,
                    'discount': record.discount,
                    'invoice_line_tax_ids': [(6, 0, record.tax_ids.ids)]

                }
                debit_vals.append((0, 0, vals))
            # TDE FIXME: what is default values(account_id,product, ??
            record = invoice_obj.create({

                'partner_id': self.patient_id.partner_id.id,
                'identification_code': self.patient_id.identification_code,
                'date_invoice': self.date,
                'invoice_line_ids': debit_vals,
                'patient_visit_id': self.id,
                'discount_type': self.discount_type_procedure,
                'discount_rate': self.discount_procedure,
                'procedure_bool': True,
            })
            record.supply_rate()
            self.procedure_invoice_id = record.id
            record.action_invoice_open()
            self.invoiced_procedure = True
            # self.write({'state': 'procedure'})

    @api.multi
    def print_order_procedure(self):
        if self.procedure_invoice_id:
            view = self.env.ref('account.invoice_form')
            context = self.env.context.copy()

            return {
                'name': _('Invoice'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context,
                'res_id': self.procedure_invoice_id.id,
            }
        if self.procedure_invoice_id:
            self.procedure_invoice_id.invoice_print()

    @api.depends('procedure_details_ids.amount')
    def compute_total_procedure_amount(self):
        for record in self:
            for item in record.procedure_details_ids:
                record.total_amount_procedure += item.amount

    @api.depends('procedure_details_ids.price_total', 'procedure_details_ids.tax_ids', 'discount_procedure',
                 'discount_type_procedure',
                 'final_total_procedure')
    def _amount_all_procedure(self):
        """
        Compute the total amounts of the Prescription.
        """
        for order in self:
            amount_tax = 0.0
            for line in order.procedure_details_ids:
                amount_tax += line.price_tax

            order.update({
                'tax_amount_procedure': amount_tax,
            })

    @api.depends('total_amount_procedure', 'discount_type_procedure', 'discount_procedure')
    def compute_final_total_amount_procedure(self):
        for record in self:
            if record.total_amount_procedure:
                if record.discount_procedure:
                    if record.discount_type_procedure == 'amount':
                        record.final_total_procedure = (record.total_amount_procedure - record.discount_procedure) + \
                                                       record.tax_amount_procedure
                    else:
                        record.final_total_procedure = (record.total_amount_procedure - (
                                (record.total_amount_procedure) * (
                                (record.discount_procedure) / 100))) + record.tax_amount_procedure
                else:
                    record.final_total_procedure = record.total_amount_procedure + record.tax_amount_procedure

    @api.multi
    def sent_procedure_to_doctor(self):
        self.write({'state': 'consultation'})
        self.write({'procedure_done': True})
        view = self.env.ref('medical_opthalmology.patient_revisit_view_tree').ids
        form_view_id = self.env.ref('medical_opthalmology.patient_revisit_view_form').ids
        if self.dilation_status == 'ref_dilation':
            self.write({'dilation_status': 'dilation_done'})
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'medical.opthalmology',
            'views': [[view, 'tree'], [form_view_id, 'form']],
            'context': {'form_view_initial_mode': 'edit', 'create': False, 'search_default_date_today': 'date_today',
                        'search_default_state': 'state'},
            'target': 'current',
        }

    def sent_procedure_to_done(self):
        self.write({'state': 'done'})

    @api.depends('procedure_invoice_id','counselling_invoice_id')
    def compute_invoice_status(self):
        for rec in self:
            rec.procedure_invoice_status = 'draft'
            if rec.procedure_invoice_id:
                rec.procedure_invoice_status = rec.procedure_invoice_id.state
            if rec.counselling_invoice_id:
                rec.procedure_invoice_status = rec.counselling_invoice_id.state


class OpticalProcedure(models.Model):
    _name = 'optical.procedure'

    procedure = fields.Many2one('product.product', required=True,
                                domain=['&', ('type', '=', 'service'), ('is_procedure', '=', True)])
    eye = fields.Selection([('left_eye', 'LE'), ('right_eye', 'RE'), ('both', 'BE')])
    patient_visit_id = fields.Many2one('medical.opthalmology', store=True)

    qty = fields.Float('Qty', default=1)
    date = fields.Date('Date')
    amount = fields.Float('Amount', force_save=True, store=True)
    space = fields.Char(' ', readonly=True, store=True)
    tax_ids = fields.Many2many('account.tax', string='Tax', store=True, domain=[('type_tax_use', '=', 'sale')])
    price_tax = fields.Float(compute='_compute_amount', string='Taxes', readonly=True, store=True)
    discount = fields.Float('Discount', readonly=False, store=True)
    sub_total = fields.Float('Sub Total', compute='compute_sub_total')
    price_total = fields.Float(compute='_compute_amount', string='Total', readonly=True, store=True)

    @api.onchange('procedure')
    def _onchange_procedures(self):
        self.amount = self.procedure.list_price

    @api.depends('procedure', 'qty', 'amount')
    def compute_sub_total(self):
        for record in self:
            record.sub_total = (record.amount) * (record.qty)

    @api.depends('qty', 'discount', 'amount', 'tax_ids', )
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.amount * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.patient_visit_id.currency_id, line.qty,
                                             product=line.procedure, partner=False)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
            })
