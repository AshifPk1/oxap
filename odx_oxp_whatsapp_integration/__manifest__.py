# -*- coding: utf-8 -*-
# Copyright 2019 GTICA C.A. - Ing Henry Vivas

{
    'name': 'OXP Whatsapp Integration',
    'summary': 'Integration Whatsapp for oxap',
    'version': '11.0',
    'category': '',
    'author': 'odox',
    'support': 'oxap@odoxsofthub.com',
    'license': 'OPL-1',
    'website': 'http://odoxsofthub.com/oxap',
    'depends': [
        'base',
        'sale_management',
        'sales_team',
        'account',
        'stock',
        'medical_opthalmology'
    ],
    'data': [
        'data/data_whatsapp_default.xml',
        'security/ir.model.access.csv',
        'views/view_whatsapp_integration.xml',
        'views/view_integration_partner.xml',
        # 'views/view_integration_invoice.xml',
        'views/view_medical_opthalmology.xml',
        # 'views/view_integration_stock_picking.xml',
        # 'views/medical_opthalmology_view.xml',
        'wizard/wizard_whatsapp_integration.xml',
    ],
    'application': True,
    'installable': True,
}
