from datetime import date
from datetime import datetime
from odoo import api, models, fields, _
from odoo.exceptions import UserError


class Counselling(models.Model):
    _inherit = 'medical.opthalmology'

    referred_to_surgery = fields.Boolean('Referred To Surgery')
    referred_to_counselling = fields.Boolean('Referred To Counselling')
    counselling_text = fields.Text('Counselling Text')
    iol_status = fields.Boolean('IOL Status', default=False)
    fitness_status = fields.Boolean('Fitness Status', default=False)
    schedule_status = fields.Boolean('Scheduling Status', default=False)
    counselling_status = fields.Selection([
        ('not_willing', 'Cold'),
        ('converted', 'Warm'),
        ('not_decided', 'Hot'),
    ], required=True, default='not_willing', ondelete='cascade', string='Status')
    surgery_date = fields.Date('Surgery Date')
    attachment_ids = fields.Many2many('ir.attachment', 'attachment_id', string='Fitness Attachments')
    total_amount = fields.Float(compute='compute_total_investigation_amount', string='Total Amount')
    discount_type = fields.Selection([
        ('amount', 'Fixed'),
        ('percent', 'Percentage')
    ])
    discount = fields.Float('Discount')
    tax_amount = fields.Float('Tax', compute='_amount_all', store=True)
    final_total = fields.Monetary(compute='compute_final_total_amount', string='Final Total')

    total_amount_surgery = fields.Float(compute='compute_total_surgery_amount', string='Total Amount')
    discount_type_surgery = fields.Selection([
        ('amount', 'Fixed'),
        ('percent', 'Percentage')
    ], string='Discount Type')
    discount_surgery = fields.Float('Discount')
    tax_amount_surgery = fields.Float('Tax', compute='_amount_all_surgery', store=True)
    final_total_surgery = fields.Float(compute='compute_final_total_surgery_amount', string='Final Total')
    counselling_details = fields.Text('   ')
    registration_invoice_number_test1 = fields.Char()
    registration_invoice_number_test2 = fields.Char()
    registration_invoice_number_test3 = fields.Char()

    @api.onchange('surgery_date')
    def _onchange_surgery_date(self):
        if self.surgery_date:
            date_surgery = datetime.strptime(self.surgery_date, "%Y-%m-%d").date()
            date_today = datetime.strptime(str(date.today()), '%Y-%m-%d').date()
            if date_surgery < date_today:
                raise UserError('Surgery date must be greater than current')

    @api.model
    def default_lens_details_id(self):
        ids = []
        for line in range(0, 0):
            data = {
                'group': self.lens_details_ids.group,
                'brand': self.lens_details_ids.brand,
                'model': self.lens_details_ids.model,
                'power': self.lens_details_ids.power,
                'item': self.lens_details_ids.item,
                'rate': self.lens_details_ids.rate,
            }
            ids.append((0, 0, data))
        return ids

    lens_details_ids = fields.One2many('optical.lens', 'patient_visit_id', string='Lens Details',
                                       default=default_lens_details_id)

    @api.model
    def default_surgery_package_ids(self):
        ids = []
        for line in range(0, 0):
            data = {
                'surgery': self.surgery_Package_ids.surgery,
                'description': self.surgery_Package_ids.description,
                'qty': self.surgery_Package_ids.qty,
                'amount': self.surgery_Package_ids.amount,
            }
            ids.append((0, 0, data))
        return ids

    surgery_Package_ids = fields.One2many('surgery.package', 'patient_visit_id', string='Lens Details',
                                          default=default_surgery_package_ids)

    @api.onchange('discount_type', 'discount', 'investigation_details_ids')
    def supply_rate_investigation(self):
        for order in self:
            if order.discount_type == 'percent':
                for line in order.investigation_details_ids:
                    line.discount = order.discount
            else:
                total = discount = 0.0
                for line in order.investigation_details_ids:
                    total += round((line.qty * line.amount))
                if order.discount != 0:
                    discount = (order.discount / total) * 100
                else:
                    discount = order.discount
                for line in order.investigation_details_ids:
                    line.discount = discount

    @api.onchange('discount_type_surgery', 'discount_surgery', 'surgery_Package_ids')
    def supply_rate(self):
        for order in self:
            if order.discount_type_surgery == 'percent':
                for line in order.surgery_Package_ids:
                    # line.discount = order.discount_surgery
                    line.update({'discount': order.discount_surgery})
            else:
                total = discount = 0.0
                for line in order.surgery_Package_ids:
                    total += round((line.qty * line.amount))
                if order.discount_surgery != 0:
                    discount = (order.discount_surgery / total) * 100
                else:
                    discount = order.discount_surgery
                for line in order.surgery_Package_ids:
                    line.update({'discount': discount})

    @api.depends('investigation_details_ids.price_total', 'investigation_details_ids.tax_ids', 'discount',
                 'discount_type',
                 'final_total')
    def _amount_all(self):
        """
        Compute the total amounts of the Prescription.
        """
        for order in self:
            amount_tax = 0.0
            for line in order.investigation_details_ids:
                amount_tax += line.price_tax
            order.update({
                'tax_amount': amount_tax,
            })

    @api.depends('surgery_Package_ids.price_total', 'surgery_Package_ids.tax_ids', 'discount_surgery',
                 'discount_type_surgery',
                 'final_total_surgery')
    def _amount_all_surgery(self):
        """
        Compute the total amounts of the Prescription.
        """
        for order in self:
            amount_tax = 0.0
            for line in order.surgery_Package_ids:
                amount_tax += line.price_tax
            order.update({
                'tax_amount_surgery': amount_tax,
            })

    @api.depends('surgery_Package_ids.amount')
    def compute_total_surgery_amount(self):
        for record in self:
            for item in record.surgery_Package_ids:
                record.total_amount_surgery += item.amount

    @api.depends('total_amount_surgery', 'tax_amount_surgery', 'discount_type_surgery', 'discount_surgery')
    def compute_final_total_surgery_amount(self):
        for record in self:
            if record.total_amount_surgery:
                if record.discount_surgery:
                    if record.discount_type_surgery == 'amount':
                        record.final_total_surgery = (
                                                             record.total_amount_surgery - record.discount_surgery) + record.tax_amount_surgery
                    else:
                        record.final_total_surgery = (record.total_amount_surgery - (record.total_amount_surgery) * (
                                record.discount_surgery / 100)) + record.tax_amount_surgery
                else:
                    record.final_total_surgery = record.total_amount_surgery + record.tax_amount_surgery

    @api.depends('investigation_details_ids.amount')
    def compute_total_investigation_amount(self):
        for record in self:
            for item in record.investigation_details_ids:
                record.total_amount += item.amount

    def sent_to_iol(self):
        self.write({'state': 'iol'})
        view = self.env.ref('medical_opthalmology.view_counselling_kanban').ids
        form_view_id = self.env.ref('medical_opthalmology.view_counselling_form').ids
        tree_view_d = self.env.ref('medical_opthalmology.counselling_tree').ids

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,form,tree',
            'res_model': 'medical.opthalmology',
            'views': [[view, 'kanban'], [form_view_id, 'form'], [tree_view_d, 'tree']],
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit', 'create': False, 'search_default_state': 'counselling',
                        'search_default_date_today': 'date_today'},
        }

    def sent_to_done(self):
        self.write({'state': 'done'})
        view = self.env.ref('medical_opthalmology.view_counselling_kanban').ids
        form_view_id = self.env.ref('medical_opthalmology.view_counselling_form').ids
        tree_view_d = self.env.ref('medical_opthalmology.counselling_tree').ids

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,form,tree',
            'res_model': 'medical.opthalmology',
            'views': [[view, 'kanban'], [form_view_id, 'form'], [tree_view_d, 'tree']],
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit', 'create': False, 'search_default_state': 'counselling',
                        'search_default_date_today': 'date_today'},
        }

    def schedule_surgery(self):
        if self.surgery_date:
            self.state = 'surgery'

    @api.onchange('total_amount', 'discount')
    def onchange_positive_values(self):
        if self.total_amount < 0:
            raise UserError(_('Total Amount must be Positive.'))
        else:
            pass
        if self.discount_type == 'percentage':
            if self.discount < 0 or self.discount > 100:
                raise UserError(_('Discount Value must be between 0 and 100 in percentage.'))
        else:
            if self.discount < 0:
                raise UserError(_('Discount Value must be positive.'))

    @api.depends('total_amount', 'discount_type', 'discount')
    def compute_final_total_amount(self):
        for record in self:
            if record.total_amount:
                if record.discount:
                    if record.discount_type == 'amount':
                        record.final_total = (record.total_amount - record.discount) + record.tax_amount
                    else:
                        record.final_total = (record.total_amount - (
                                record.total_amount * (record.discount / 100))) + record.tax_amount
                else:
                    record.final_total = record.total_amount + record.tax_amount

    def default_stage_id(self):
        sub_state = self.env['counselling.substate'].search([('is_start', '=', True)], limit=1)
        return \
            sub_state

    sub_state_id = fields.Many2one('counselling.substate', string='Sub State', default=default_stage_id)

    @api.multi
    def create_order(self):
        debit_vals = []
        invoice_obj = self.env['account.invoice'].sudo()
        if not self.counselling_invoice_id:
            for record in self.investigation_details_ids:
                account = record.investigation.property_account_income_id or record.investigation.categ_id.property_account_income_categ_id
                if not account:
                    raise UserError(
                        _('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                        (record.investigation.name, record.investigation.id, record.investigation.categ_id.name))

                vals = {
                    'name': record.investigation.name,
                    'quantity': record.qty,
                    'uom_id': 1,
                    'product_id': record.investigation.id,
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
                'discount_type': self.discount_type,
                'discount_rate': self.discount,
                'investigation_bool': True,
            })
            record.supply_rate()
            self.counselling_invoice_id = record.id
            record.action_invoice_open()
            self.invoiced_investigation = True

    @api.multi
    def print_order(self):
        if self.counselling_invoice_id:
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
                'res_id': self.counselling_invoice_id.id,
            }
        if self.counselling_invoice_id:
            self.counselling_invoice_id.invoice_print()

    @api.multi
    def create_order_surgery(self):
        debit_vals = []
        sale_vals = []
        invoice_obj = self.env['account.invoice']
        sale_obj = self.env['sale.order']
        if not self.surgery_invoice_id:
            for record in self.surgery_Package_ids:
                account = record.surgery.property_account_income_id or record.surgery.categ_id.property_account_income_categ_id
                if not account:
                    raise UserError(
                        _('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                        (record.surgery.name, record.surgery.id, record.surgery.categ_id.name))
                invoice_vals = {
                    'name': record.surgery.name,
                    'quantity': record.qty,
                    'uom_id': 1,
                    'product_id': record.surgery.id,
                    'account_id': account.id,
                    'price_unit': record.amount,
                    'discount': record.discount,
                    'invoice_line_tax_ids': [(6, 0, record.tax_ids.ids)]
                }
                debit_vals.append((0, 0, invoice_vals))
            record = invoice_obj.create({
                'partner_id': self.patient_id.partner_id.id,
                'identification_code': self.patient_id.identification_code,
                'date_invoice': self.date,
                'discount_type': self.discount_type_surgery,
                'discount_rate': self.discount_surgery,
                'invoice_line_ids': debit_vals,
                'patient_visit_id': self.id,
                'surgery_bool': True,

            })
            record.supply_rate()
            self.surgery_invoice_id = record.id
            record.action_invoice_open()
            self.invoiced_surgery = True
            if self.lens_details_ids:
                for record in self.lens_details_ids:
                    sale_vals_dict = {
                        'name': record.model.name,
                        'product_uom_qty': record.qty,
                        'product_uom': 1,
                        'product_id': record.model.id,
                        'price_unit': record.rate,
                    }
                    sale_vals.append((0, 0, sale_vals_dict))
                    # TDE FIXME: what is default values(account_id,product, ??
                record = sale_obj.create({
                    'partner_id': self.patient_id.partner_id.id,
                    'identification_code': self.patient_id.identification_code,
                    'date': self.date,
                    'order_line': sale_vals,
                    'patient_visit_id': self.id,
                })
                record.action_confirm()

    @api.multi
    def print_order_surgery(self):

        if self.surgery_invoice_id:
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
                'res_id': self.surgery_invoice_id.id,
            }
        if self.surgery_invoice_id:
            self.surgery_invoice_id.invoice_print()

    def confirm_counselling_appoitment(self):
        view = self.env.ref('medical_opthalmology.counselling_wizard_view')
        context = self.env.context.copy()

        return {
            'name': _('Create Appointment'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'counselling.appointment',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
        }

    @api.multi
    def print_medical_report(self):
        data_dict = {'datas': self.id}
        return self.env.ref('medical_opthalmology.medical_detail_template').report_action([], data=data_dict)

    @api.multi
    def print_medical_report_wo_header(self):
        data_dict = {'datas': self.id}
        return self.env.ref('medical_opthalmology.medical_detail_template_wo_header').report_action([], data=data_dict)


    def create_procedure(self):
        self.write({'state': 'procedure'})
        self.write({'procedure_type': 'treatment'})
