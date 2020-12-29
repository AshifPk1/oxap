# !/usr/bin/env python
# -*- coding: utf-8 -*-
{
    'name': 'Purchase Total Discount',
    'version': '1.0',
    'author': 'MNP',
    'description': """
    """,
    'website': 'https://www.odootec.com/',
    'depends': ['purchase', 'sale_discount_total'],
    'data': [
        'views/purchase_view.xml',
        'views/invoice_view.xml'

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
