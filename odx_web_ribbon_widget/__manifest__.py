# -*- encoding: utf-8 -*-
{
    'name': 'ODX RIBBON WIDGET (OXP)',
    'version': '11.0.1.0.0',
    'author': 'Odox SoftHub',
    'website': 'http://www.odoxsofthub.com',
    'category': 'base',
    'depends': ['base', 'web'],
    'summary': 'Introduce Ribbon Widget ',
    'data': [
        'views/base_view.xml'

    ],
    'qweb': [
        "static/src/xml/ribbon.xml",
    ],
    'installable': True,
    'auto_install': False,
}
