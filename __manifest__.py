# -*- coding: utf-8 -*-
{
    'name': "Consultar existencias",

    'summary': """
    Verifica la existencia de productos""",

    'description': """
    Verifica la existencia de productos
    """,

    'author': "DGV",
    'website': "https://github.com/AlfaSystemas5457/check_stock",
    'category': 'Stock',
    'version': '1.1',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/check_stock_partial_validation_wizard_view.xml',
        'views/check_stock_no_stock_view.xml',
        'views/button_parcial_stock_view.xml',
    ],
    'instalable': True
}