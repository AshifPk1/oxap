# -*- coding: utf-8 -*-
from odoo import models, api


class MedicalReport(models.AbstractModel):
    _name = 'report.oxap_reports.pharmacy_revenue_report_template'

    @api.multi
    def get_report_values(self, docids, data=None):
        docs = []
        doctor_id = data['form']['doctor_id']
        date_start = data['form']['date_from']
        date_end = data['form']['date_to']
        doctor_name = data['form']['doctor_name']
        from_date = data['form']['date_from'] + ' ' + '00:00:00'
        to_date = data['form']['date_to'] + ' ' + '23:59:59'

        total_patients = self.env['account.invoice'].search_count([('doctor_id', '=', doctor_id),
                                                                   ('date_invoice', '>=', from_date),
                                                                   ('date_invoice', '<=', to_date),
                                                                   ('registration_bool', '=', True), ])

        records = self.env['account.invoice'].search([('doctor_id', '=', doctor_id),
                                                      ('date_invoice', '>=', from_date),
                                                      ('date_invoice', '<=', to_date),
                                                      ('registration_bool', '=', True),
                                                      ('reconciled', '=', True), ])
        reg_total = 0
        for r in records:
            reg_total = reg_total + r.amount_total

        pharmacy_record = self.env['medical.pharmacy'].search_count([('doctor_id', '=', doctor_id),
                                                                    ('date', '>=', from_date),
                                                                    ('date', '<=', to_date), ])

        pharmacy_prescription = self.env['account.invoice'].search([('doctor_id', '=', doctor_id),
                                                                    ('date_invoice', '>=', from_date),
                                                                    ('date_invoice', '<=', to_date),
                                                                    ('pharmacy_bool', '=', True),
                                                                    ('reconciled', '=', True), ])
        total_amount = 0
        for rec in pharmacy_prescription:
            total_amount = total_amount + rec.amount_total
            round(total_amount, 2)

        work_orders = self.env['optics.work.order'].search_count([('doctor_id', '=', doctor_id),
                                                                ('date', '>=', from_date),
                                                                ('date', '<=', to_date)])

        orders = self.env['account.invoice'].search([('doctor_id', '=', doctor_id),
                                                     ('date_invoice', '>=', from_date),
                                                     ('date_invoice', '<=', to_date),
                                                     ('optics_bool', '=', True),
                                                     ('reconciled', '=', True), ])
        work_order_total = 0
        for rec in orders:
            work_order_total = work_order_total + rec.amount_total

        investigations = self.env['account.invoice'].search_count([('doctor_id', '=', doctor_id),
                                                                   ('date_invoice', '>=', from_date),
                                                                   ('date_invoice', '<=', to_date),
                                                                   ('investigation_bool', '=', True), ])

        investigations_rec = self.env['account.invoice'].search([('doctor_id', '=', doctor_id),
                                                                 ('date_invoice', '>=', from_date),
                                                                 ('date_invoice', '<=', to_date),
                                                                 ('investigation_bool', '=', True),
                                                                 ('reconciled', '=', True), ])
        investigation_total = 0
        for rec in investigations_rec:
            investigation_total = investigation_total + rec.amount_total

        surgery = self.env['account.invoice'].search_count([('doctor_id', '=', doctor_id),
                                                            ('date_invoice', '>=', from_date),
                                                            ('date_invoice', '<=', to_date),
                                                            ('surgery_bool', '=', True), ])

        surgery_amount = self.env['account.invoice'].search([('doctor_id', '=', doctor_id),
                                                             ('date_invoice', '>=', from_date),
                                                             ('date_invoice', '<=', to_date),
                                                             ('surgery_bool', '=', True),
                                                             ('reconciled', '=', True), ])

        surgery_total = 0
        for rec in surgery_amount:
            surgery_total = surgery_total + rec.amount_total

        grand_total = reg_total + investigation_total + work_order_total + total_amount + surgery_total


        round(grand_total, 2)

        docs.append({
            'registrations': total_patients,
            'registration_total': reg_total,
            'investigations': investigations,
            'investigation_total': investigation_total,
            'pharmacy_prescribed': pharmacy_record,
            'total_amount': total_amount,
            'work_orders': work_orders,
            'work_order_total': work_order_total,
            'surgery': surgery,
            'surgery_total': surgery_total,
            'grand_total': grand_total
        })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_from': date_start,
            'date_to': date_end,
            'doctor_name': doctor_name,
            'docs': docs,
        }
