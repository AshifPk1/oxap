# -*- coding: utf-8 -*-
#
# Odootec <http://www.odootec.com>, Copyright (C) 2015 - Today.
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY

from odoo import api, models
from odoo.tools.misc import formatLang, DEFAULT_SERVER_DATETIME_FORMAT


class HrPayslipParser(models.AbstractModel):
    _name = 'report.odx_payslip_report.hr_payslip_report'
    from_date = ''
    to_date = ''
    employee_ids = False
    salary_rule_ids = False

    def _get_data(self, data):
        self.from_date = data['form']['start_date']
        self.to_date = data['form']['end_date']
        self.employee_ids = data['form']['employee_ids']
        self.salary_rule_ids = self.env['hr.salary.rule'].browse(data['form']['salary_rule_ids']).sorted(
            key=lambda v: v.sequence)
        column_headings = self._get_salary_rule_names()
        data, payrule_total = self._get_table_data()
        total_list = ['Total']
        for rule in self.salary_rule_ids:
            total_list.append(payrule_total.get(rule.id, 0.0))
        res = {'column_headings': column_headings,
               'data': data,
               'total': total_list
               }
        return res

    def _get_salary_rule_names(self):
        rules = self.salary_rule_ids
        rule_names = ['Employee']
        for rule in rules:
            rule_names.append(rule.code.replace(" ", "\n"))
        return rule_names

    def _get_table_data(self):
        payslip_obj = self.env['hr.payslip']
        employee_obj = self.env['hr.employee']
        data = []
        payrule_total = {}

        for employee in self.employee_ids:
            employ = employee_obj.browse(employee)

            payslip_ids = payslip_obj.search([('employee_id', '=', employee),
                                              ('date_from', '<=', self.to_date),
                                              ('date_from', '>=', self.from_date)])
            if not payslip_ids:
                continue
            for payslip in payslip_ids:
                refund = False
                if payslip.credit_note:
                    refund = True
                data_list = [employ.name]
                payslip_lines_ids = payslip.line_ids
                if not payslip_lines_ids:
                    continue
                for rule_id in self.salary_rule_ids:
                    rule_found = False
                    for payslip_line_rec in payslip_lines_ids:
                        if payslip_line_rec.salary_rule_id.id == rule_id.id:
                            if refund:
                                amount = -payslip_line_rec.total
                            else:
                                amount = payslip_line_rec.total
                            data_list.append(amount)
                            rule_found = True
                            # if payrule_total.has_key(rule_id.id):
                            if rule_id.id in payrule_total:
                                payrule_total[rule_id.id] += amount
                            else:
                                payrule_total[rule_id.id] = amount
                    if not rule_found:
                        data_list.append(0.00)
                data.append(data_list)

        return data, payrule_total

    @api.model
    def get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        date_from = data['form']['start_date']
        date_to = data['form']['end_date']
        val = ''
        if date_from and date_to:
            date_from = datetime.strptime(date_from, DEFAULT_SERVER_DATETIME_FORMAT)
            date_to = datetime.strptime(date_to, DEFAULT_SERVER_DATETIME_FORMAT)
            dates = [dt for dt in rrule(MONTHLY, dtstart=date_from, until=date_to)]
            for record in dates:
                val += record.strftime("%B") + "/" + record.strftime("%Y") + "-"
        elif date_from and not date_to:
            my_date = datetime.strptime(date_from, DEFAULT_SERVER_DATETIME_FORMAT)
            val = (str(my_date.strftime("%B")) + '/' +
                   str(my_date.strftime("%Y")))
        elif not date_from and date_to:
            my_date = datetime.strptime(date_to, DEFAULT_SERVER_DATETIME_FORMAT)
            val = (str(my_date.strftime("%B")) + '/' +
                   str(my_date.strftime("%Y")))
        else:
            val = ''

        get_data = self._get_data(data)
        docargs = {
            'doc_ids': docids,
            'get_data': get_data,
            'doc_model': model,
            'date_from': date_from,
            'date_to': date_to,
            'date_word': val,
            'data': data,
            'docs': docs,
            'formatLang': formatLang
        }
        return docargs
