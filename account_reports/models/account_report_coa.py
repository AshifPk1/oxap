# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import models, api, _


class report_account_coa(models.AbstractModel):
    _name = "account.coa.report"
    _description = "Chart of Account Report"
    _inherit = "account.general.ledger"

    filter_date = {'date_from': '', 'date_to': '', 'filter': 'this_month'}
    filter_comparison = {'date_from': '', 'date_to': '', 'filter': 'no_comparison', 'number_period': 1}
    filter_cash_basis = False
    filter_all_entries = False
    filter_hierarchy = False
    filter_unfold_all = None

    def get_templates(self):
        templates = super(report_account_coa, self).get_templates()
        templates['main_template'] = 'account_reports.template_coa_report'
        return templates

    def get_columns_name(self, options):
        columns = [
            {'name': ''},
            {'name': _('Debit'), 'class': 'number'},
            {'name': _('Credit'), 'class': 'number'},
        ]
        if options.get('comparison') and options['comparison'].get('periods'):
            columns += [
                           {'name': _('Debit'), 'class': 'number'},
                           {'name': _('Credit'), 'class': 'number'},
                       ] * len(options['comparison']['periods'])
        return columns + [
            {'name': _('Debit'), 'class': 'number'},
            {'name': _('Credit'), 'class': 'number'},
            {'name': _('Debit'), 'class': 'number'},
            {'name': _('Credit'), 'class': 'number'},
        ]

    def _post_process(self, grouped_accounts, res, options, comparison_table):
        lines = []
        context = self.env.context
        company_id = context.get('company_id') or self.env.user.company_id
        title_index = ''
        sorted_accounts = sorted(grouped_accounts, key=lambda a: a.code)
        zero_value = ''
        sum_columns = [0, 0, 0, 0]
        for period in range(len(comparison_table)):
            sum_columns += [0, 0]
        for account in sorted_accounts:
            initial_balance_debit = res[account]['initial_bal']['debit']
            initial_balance_credit = res[account]['initial_bal']['credit']
            sum_columns[0] += initial_balance_debit  # if initial_balance_debit > 0 else 0
            sum_columns[1] += initial_balance_credit  # if initial_balance_credit < 0 else 0
            cols = [
                {'name': self.format_value(initial_balance_debit), 'no_format_name': initial_balance_debit},
                {'name': self.format_value(initial_balance_credit), 'no_format_name': initial_balance_credit},
            ]
            total_period_debit = 0
            total_period_credit = 0
            for period in range(len(comparison_table)):
                amount_debit = grouped_accounts[account][period]['debit']
                amount_credit = grouped_accounts[account][period]['credit']
                total_period_debit += amount_debit
                total_period_credit += amount_credit
                cols += [{'name': self.format_value(amount_debit), 'no_format_name': amount_debit},
                         {'name': self.format_value(amount_credit), 'no_format_name': amount_credit}]
                p_indice = period * 2 if period > 1 else 3
                p_indice = 1 if period == 0 else p_indice
                sum_columns[(p_indice) + 1] += amount_debit  # if amount_debit > 0 else 0
                sum_columns[(p_indice) + 2] += amount_credit  # if amount_credit < 0 else 0

            total_amount_debit = initial_balance_debit + total_period_debit
            total_amount_credit = initial_balance_credit + total_period_credit
            sum_columns[-2] += total_amount_debit  # if total_amount_debit > 0 else 0
            sum_columns[-1] += total_amount_credit  # if total_amount_credit < 0 else 0

            cols += [
                {'name': self.format_value(total_amount_debit), 'no_format_name': total_amount_debit},
                {'name': self.format_value(total_amount_credit), 'no_format_name': total_amount_credit},
            ]
            lines.append({
                'id': account.id,
                'name': account.code + " " + account.name,
                'columns': cols,
                'unfoldable': False,
                'caret_options': 'account.account',
            })
        lines.append({
            'id': 'grouped_accounts_total',
            'name': _('Total'),
            'class': 'o_account_reports_domain_total',
            'columns': [{'name': self.format_value(v)} for v in sum_columns],
            'level': 0,
        })
        return lines

    @api.model
    def get_lines(self, options, line_id=None):
        context = self.env.context
        company_id = context.get('company_id') or self.env.user.company_id
        grouped_accounts = {}
        initial_balances_debit = {}
        initial_balances_credit = {}
        comparison_table = [options.get('date')]
        comparison_table += options.get('comparison') and options['comparison'].get('periods') or []

        # get the balance of accounts for each period
        period_number = 0
        for period in reversed(comparison_table):
            res = self.with_context(date_from_aml=period['date_from'], date_to=period['date_to'],
                                    date_from=period['date_from'] and company_id.compute_fiscalyear_dates(
                                        datetime.strptime(period['date_from'], "%Y-%m-%d"))[
                                        'date_from'] or None).group_by_account_id(options,
                                                                                  line_id)  # Aml go back to the beginning of the user chosen range but the amount on the account line should go back to either the beginning of the fy or the beginning of times depending on the account
            if period_number == 0:
                initial_balances_debit = dict([(k, res[k]['initial_bal']['debit']) for k in res])
                initial_balances_credit = dict([(k, res[k]['initial_bal']['credit']) for k in res])
            for account in res:
                if account not in grouped_accounts:
                    grouped_accounts[account] = [{'balance': 0, 'debit': 0, 'credit': 0} for p in comparison_table]
                grouped_accounts[account][period_number]['balance'] = res[account]['balance'] - \
                                                                      res[account]['initial_bal']['balance']
                grouped_accounts[account][period_number]['debit'] = res[account]['debit'] - res[account]['initial_bal'][
                    'debit']
                grouped_accounts[account][period_number]['credit'] = res[account]['credit'] - \
                                                                     res[account]['initial_bal']['credit']
            period_number += 1

        # build the report
        lines = self._post_process(grouped_accounts, res, options, comparison_table)
        return lines

    @api.model
    def get_report_name(self):
        return _("Trial Balance")
