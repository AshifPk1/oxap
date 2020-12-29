from odoo import api, models, fields, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError


class MedicalPharmacy(models.Model):
    _name = 'medical.pharmacy'
    _description = 'Pharmacy Details'
    _rec_name = 'sequence'
    _order = 'sequence desc'

    @api.model
    def create(self, vals):
        if not vals.get('sequence'):
            if 'patient_id' in vals:
                vals['sequence'] = self.env['ir.sequence'].next_by_code(
                    'medical.pharmacy') or _('New')
        return super(MedicalPharmacy, self).create(vals)

    name = fields.Char(string='Patient Reference', copy=False, readonly=True, index=True)

    sequence = fields.Char(required=True, copy=False, readonly=True, index=True,
                           ondelete='cascade', default=lambda self: _('New'), )

    new_patient_is = fields.Boolean('New Patient')

    patient_new = fields.Char(string='New Patient')

    patient_id = fields.Many2one('medical.patient', string='Patient Name', required=True)

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True,
                                   help="Pricelist for current sales order.", default=1)

    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True,
                                  required=True)

    phone = fields.Char('Contact Number', related='patient_id.phone', required=True)

    city = fields.Char(related='patient_id.city')

    zip = fields.Char(change_default=True, related='patient_id.zip')

    birthdate_date = fields.Date('Birth Date', related='patient_id.birthdate_date', required=True)

    street = fields.Char(related='patient_id.street')

    street2 = fields.Char(related='patient_id.street2')

    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', related='patient_id.state_id')

    identification_code = fields.Char('File Number', related='patient_id.identification_code', store=True)

    age = fields.Char('Age')

    search_file_number = fields.Char('Search File Number')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], related='patient_id.gender')

    state = fields.Selection(related='work_order_id.state', string='Status', default='draft', copy=False)

    re_state = fields.Selection([
        ('draft', 'draft'),
        ('processed', 'processed'),
        ('done', 'Done')
    ], string='Restate', default='draft')

    date = fields.Datetime('Admission Date', default=fields.Datetime.now)

    date_today = fields.Date('Date', default=fields.Date.context_today, readonly=True, )

    doctor_id = fields.Many2one('medical.practitioner', string='Doctor')

    glass_prescription = fields.Text('Glass Prescription')

    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', related='patient_id.country_id')

    tag_ids = fields.Many2many('patient.visit.tag', string='Tags', )

    tax_ids = fields.Many2many('account.tax', string='Tax')

    total_amount = fields.Float('Total Amount', compute='compute_total_optics_amount')

    paid_amount = fields.Float(string='Paid Amount')
    balance_amount = fields.Float(string='Balance Amount', compute='compute_balance_amount')

    discount_type = fields.Selection([
        ('amount', 'Fixed'),
        ('percent', 'Percentage')
    ])
    discount = fields.Float('Discount')
    final_total = fields.Float(string='Final Total', compute='compute_final_total_amount')

    doctor_prescription = fields.Text('Prescription')

    work_order_id = fields.Many2one('pharmacy.work.order')

    tax_amount = fields.Float('Tax', compute='_amount_all', store=True)

    referred_by_id = fields.Many2one('reference.from', 'Reference From')

    reference_type_id = fields.Many2one('reference.type', 'Reference Type')

    medicine_ids = fields.One2many('doctor.treatment', 'pharmacy_id', readonly=1)

    treatment_status = fields.Boolean('Treatment Status', default=False)

    invoice_count = fields.Integer(string='# of Invoices', related='work_order_id.order_id.invoice_count',
                                   readonly=True)

    is_refunded = fields.Boolean('Refunded')

    @api.multi
    def unlink(self):
        res = super(MedicalPharmacy, self).unlink()
        raise UserError("You can't delete the Prescripton.")


    @api.multi
    def copy(self, default=None):
        rec = super(MedicalPharmacy, self).copy(default)
        raise UserError(_('You cannot duplicate a Prescripton.'))

    @api.multi
    def action_view_invoice(self):
        if self.work_order_id:
            if self.work_order_id.order_id:
                invoices = self.work_order_id.order_id.invoice_ids
                action = self.env.ref('account.action_invoice_tree1').read()[0]
                if len(invoices) > 1:
                    action['domain'] = [('id', 'in', invoices.ids)]
                elif len(invoices) == 1:
                    action['views'] = [(self.env.ref('account.invoice_form').id, 'form')]
                    action['res_id'] = invoices.ids[0]
                else:
                    action = {'type': 'ir.actions.act_window_close'}
                return action

    @api.onchange('phone')
    def _onchange_phone(self):
        if self.phone and not self.new_patient_is and not self.identification_code:

            patient_ids = self.env['medical.patient'].search([('phone', '=', self.phone)])
            if patient_ids:
                patient_id = patient_ids[0]
                self.patient_id = patient_id.id
                self.identification_code = patient_id.identification_code
                self.age = patient_id.patient_age
                self.gender = patient_id.gender
                self.street = patient_id.street
                return {'domain': {'patient_id': [('id', '=', patient_ids.ids)]}}

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

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.phone = self.patient_id.phone
        self.identification_code = self.patient_id.identification_code
        self.gender = self.patient_id.gender
        self.street = self.patient_id.street
        self.age = self.patient_id.patient_age

    @api.onchange('date')
    def _onchange_admission_date(self):
        if self.date:
            date_admision = datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S").date()
            date_today = date.today()
            if date_admision < date_today:
                raise UserError('Admission date must be greater than current')

    @api.model
    def default_pharmacy_ids(self):
        ids = []
        for line in range(0, 0):
            data = {
                'product_id': self.product_id.id,
                'categ_id': self.product_id.default_code,
                'quantity': self.quantity,
                'price_unit': self.price_unit,
                'sub_total': self.sub_total,
            }
            ids.append((0, 0, data))
        return ids

    pharmacy_details_ids = fields.One2many('pharmacy.prescription', 'patient_visit_id', string='Pharmacy Details',
                                           default=default_pharmacy_ids)

    @api.depends('pharmacy_details_ids.price_unit', 'pharmacy_details_ids.quantity')
    def compute_total_optics_amount(self):
        for record in self:
            for item in record.pharmacy_details_ids:
                record.total_amount += (item.price_unit) * (item.quantity)

    @api.onchange('discount_type', 'discount', 'pharmacy_details_ids')
    def supply_rate(self):
        for order in self:
            if order.discount_type == 'percent':
                for line in order.pharmacy_details_ids:
                    line.discount = order.discount
            else:
                total = discount = 0.0
                for line in order.pharmacy_details_ids:
                    total += round((line.quantity * line.price_unit))
                if order.discount != 0:
                    discount = (order.discount / total) * 100
                else:
                    discount = order.discount
                for line in order.pharmacy_details_ids:
                    line.discount = discount

    @api.depends('total_amount', 'discount_type', 'discount')
    def compute_final_total_amount(self):
        for record in self:
            if record.total_amount:
                if record.discount:
                    if record.discount_type == 'amount':
                        record.final_total = (record.total_amount - record.discount) + record.tax_amount
                    else:
                        record.final_total = (record.total_amount - (
                                (record.total_amount) * ((record.discount) / 100))) + record.tax_amount
                else:
                    record.final_total = record.total_amount + record.tax_amount

    @api.depends('pharmacy_details_ids.price_total', 'pharmacy_details_ids.tax_ids', 'discount', 'discount_type',
                 'final_total')
    def _amount_all(self):
        """
        Compute the total amounts of the Prescription.
        """
        for order in self:
            amount_tax = 0.0
            for line in order.pharmacy_details_ids:
                amount_tax += line.price_tax
            order.update({
                'tax_amount': amount_tax,
            })

    @api.depends('paid_amount')
    def compute_balance_amount(self):
        for record in self:
            if record.paid_amount:
                record.balance_amount = record.paid_amount - record.final_total

    def create_work_order(self):
        debit_vals = []
        for record in self.pharmacy_details_ids:
            if record.quantity:
                if not record.qty_available:
                    raise ValidationError("No sufficient stock Quantity to proceed")
                if record.qty_available:
                    if record.quantity > record.qty_available:
                        raise ValidationError('Only %s quantity in stock' % record.qty_available)
            if record.lot_number_id:
                if not record.lot_number_id.qty_available:
                    raise ValidationError("No sufficient stock Quantity to proceed")
                if record.qty_available:
                    if record.quantity > record.lot_number_id.qty_available:
                        raise ValidationError('Only %s quantity in stock' % record.lot_number_id.qty_available)

            vals = {
                'name': record.product_id.name,
                'product_uom_qty': record.quantity,
                'qty_to_invoice': record.quantity,
                'lot_number_id': record.lot_number_id.id,
                'price_unit': record.price_unit,
                'doctor_id': self.doctor_id.id,
                'product_id': record.product_id.id,
                'price_subtotal': record.sub_total,
                'tax_id': [(6, 0, record.tax_ids.ids)]
            }
            debit_vals.append((0, 0, vals))

        record = self.env['pharmacy.work.order'].create(
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

            })
        record.order_id.supply_rate()
        self.work_order_id = record.id
        record.order_id.doctor_id = self.doctor_id.id
        record.order_id.action_confirm()
        for pickings in record.picking_ids:
            pickings.button_validate()
        invoices = record.order_id.action_invoice_create()
        for invoice in record.order_id.invoice_ids:
            invoice.pharmacy_bool = True
            invoice.identification_code = self.identification_code
            invoice.doctor_id = self.doctor_id.id
            invoice.sale_order_id = self.work_order_id.order_id.id
        self.state = 'invoiced'
        self.re_state = 'done'

        inv_obj = self.env['pharmacy.work.order'].search([('id', '=', self.work_order_id.id)])
        return inv_obj.registerpayment()

    def print_invoice(self):
        return self.env.ref('medical_pharmacy.report_pharmacy_print').report_action(self)
        # record = self.env['pharmacy.work.order'].search([('id','=',self.work_order_id.id)])
        # return record.print_invoice()

    # @api.multi
    # def register_payment(self):
    #     record = self.env['pharmacy.work.order'].search([('id', '=', self.work_order_id.id)])
    #     return record.registerpayment()

    @api.onchange('patient_new')
    def on_change_patient_new(self):
        if self.patient_new:
            patient = self.env['medical.patient'].create({'name': self.patient_new})
            self.patient_id = patient.id

    @api.multi
    def credit_note_pharmacy(self):
        description = 'refund'
        date = fields.Date.today() or False
        refund = False
        if self.work_order_id:
            if self.work_order_id.order_id:

                # Create Credite note
                if self.work_order_id.order_id.invoice_ids:
                    invoices = self.work_order_id.order_id.invoice_ids
                    for inv in invoices:
                        description = description or inv.name
                        try:
                            refund = inv.refund(date, date, description, inv.journal_id.id)
                            self.is_refunded = True
                        except:
                            raise UserError(('Credit Note Already Created'))

                # Create Return Order
                if self.work_order_id.order_id.picking_ids:
                    for picking in self.work_order_id.order_id.picking_ids:
                        wizard = self.env['stock.return.picking'].with_context({
                            'active_id': picking.id
                        }).create({'picking_id': picking.id})
                        return_picking = wizard.create_returns()
                        return_picking_id = picking.search([('id', '=', return_picking['res_id'])])
                        for return_lines in return_picking_id.move_line_ids:
                            for line in picking.move_line_ids:
                                if return_lines.product_id == line.product_id:
                                    return_lines.lot_id = line.lot_id.id if line.lot_id else False
                        if return_picking_id:
                            return_picking_id.button_validate()
                        for move in return_picking_id.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                            for move_line in move.move_line_ids:
                                move_line.qty_done = move_line.product_uom_qty
                        if return_picking_id:
                            return_picking_id.action_done()

                if refund:
                    for invoice in refund:
                        invoice.pharmacy_bool = True
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

    picking_count = fields.Integer(string='Picking Error', compute='_compute_picking_count')

    @api.depends('work_order_id.picking_ids')
    def _compute_picking_count(self):
        for records in self:
            for picking in records.work_order_id:
                count = 0
                if picking.picking_ids:
                    for rec in picking.picking_ids:
                        if rec.state != 'done':
                            count += 1
                    records.picking_count = count

    @api.multi
    def picking_error(self):
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        result['context'] = {}
        pick_ids = self.mapped('work_order_id.picking_ids').filtered(lambda picks: picks.state not in ('done'))
        # choose the view_mode
        if not pick_ids or len(pick_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % (pick_ids.ids)
        elif len(pick_ids) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            result['domain'] = [('state', 'not in', ('done'))]
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = pick_ids.id
        return result

    def print_prescription(self):
        if self.medicine_ids or self.doctor_prescription:
            return self.env.ref('medical_pharmacy.print_prescription_report').report_action(self)
        else:
            raise UserError("There is no medications data to print")


# lot id passing to invoice
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update({'lot_id': self.lot_number_id.id})
        return res
