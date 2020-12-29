# -*- encoding: utf-8 -*-

{
    'name': 'Oxap Web Login Screen',
    'summary': 'OXAP Web Login Screen',
    'version': '11.0.1.0',
    'category': 'Website',
    'summary': """
   Oxap Odoo Web Login Screen
""",
    'author': "odoxsofthub",
    'website': 'http://www.odoxsofthub.com',
    'depends': ['web'
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'templates/website_templates.xml',
        'templates/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/web_export_view_template.xml",
    ],

    'installable': True,
    'application': True,
}
