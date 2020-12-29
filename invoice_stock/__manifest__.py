# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Ivoice and Warehouse Management',
    'version': '1.0',
    'category': 'Hidden',
    'summary': 'Quotation, Sales Orders, Delivery & Invoicing Control',
    'description': """
Manage sales quotations and orders
==================================

This module makes the link between the sales and warehouses management applications.

Preferences
-----------
* Shipping: Choice of delivery at once or partial delivery
* Invoicing: choose how invoices will be paid
* Incoterms: International Commercial terms

You can choose flexible invoicing methods:

* *On Demand*: Invoices are created manually from Sales Orders when needed
* *On Delivery Order*: Invoices are generated from picking (delivery)
* *Before Delivery*: A Draft invoice is created and must be paid before delivery
""",
    'website': 'https://www.odoo.com/page/warehouse',
    'depends': ['sale_management', 'stock_account','account'],
    'data': [
        'views/account_invoice_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
}
