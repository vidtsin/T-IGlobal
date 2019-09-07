# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.
{
    'name' : 'Custom Stock',
    'version': '12.0',
    'author': 'PPTS [India] Pvt.Ltd.',
    'category': 'Stock',
    'website': 'https://www.pptssolutions.com',
    'summary': 'Product Stock Location',
    'description': """ Product Stock Count  """,
    'depends': [
        'purchase','product','sale','stock','base',
    ],
    'data': [
        'views/stock_product_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}