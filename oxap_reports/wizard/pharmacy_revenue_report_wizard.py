# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PatientNumberReport(models.TransientModel):
    _name = 'pharmacy.revenue.report.wiz'

    date_from = fields.Date('From')
    date_to = fields.Date('To')
    doctor_id = fields.Many2one('medical.practitioner', string='Doctor')
    doctor_name = fields.Char('name')

    @api.multi
    def print_pharmacy_revenue_report(self):
        self.doctor_name = self.doctor_id.name
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'doctor_id': self.doctor_id.id,
                'doctor_name': self.doctor_name,
            },
        }

        # from_date = self.date_from + ' ' + '00:00:00'
        # to_date = self.date_to + ' ' + '23:59:59'
        # doctor_id=self.doctor_id.id
        # pharmacy_record = self.env['medical.pharmacy'].search([('doctor_id', '=', doctor_id),
        #                                                              ('date', '>=', from_date),
        #                                                              ('date', '<=', to_date),
        #                                                              ])
        #
        # print(from_date,to_date,doctor_id)
        # for r in pharmacy_record:
        #        print("pharma",r.final_total)
        # surgery = self.env['medical.opthalmology'].search([('doctor_id', '=', doctor_id),
        #                                                              ('date', '>=', from_date),
        #                                                              ('date', '<=', to_date),
        #                                                               ('surgery_bool','=',True)
        #                                                              ])
        # print("surgery",surgery)

        return self.env.ref('oxap_reports.pharmacy_revenue_report').report_action(self, data=data)
