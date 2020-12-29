{
    'name': "lot / serial Report",
    'version': '5.0.4',
    'category': 'Stock',
    'price': '10',
    'sequence': 0,
    'depends': [
        'base',
        'stock',
        'send_expiry_lot_mail',
        # 'intecompany_fixed_date_expect',
    ],
    'demo': [],
    'data': [
        # 'odt_sale_security/ir.model.access.csv',
        'reports/stock_production_lot.xml',
        'reports/stock_production_lot_analytic.xml',

    ],
    'qweb': [
    ],
    "currency": 'EUR',
    'installable': True,
    'application': True,

    # "license": "OPL-1",
}
