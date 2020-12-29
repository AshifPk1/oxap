{
    'name': "Product Request",

    'summary': "product request",
    'author': "Odox Softhub",
    'category': '',
    'version': '0.1',

    'depends': ['base', 'purchase'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_request_view.xml',
        'data/sequence.xml',

    ],

}
