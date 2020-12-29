# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#
#    This program is free software: you can redistribute it and/or modify
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
##############################################################################


{
    'name': 'Payslip Report',
    'version': '11.0.1.0.0',
    'category': 'HR',
    'description': """
Payroll report 
""",
    'author': 'Odox SoftHub',
    'website': 'http://www.odoxsofthub.com',
    'depends': ['hr', 'hr_payroll_account'],
    'data': [
        'security/ir.model.access.csv',
        'views/new_header.xml',
        'views/hr_payslip_report.xml',
        'views/hr_payslip_report_template_view.xml',
        'wizard/payroll_analysis_view.xml',
        'report.xml',

    ],
    'installable': True,
}
