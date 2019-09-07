# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.
{
    'name' : 'Custom Purchase',
    'version': '12.0',
    'author': 'PPTS [India] Pvt.Ltd.',
    'category': 'Purchase',
    'website': 'https://www.pptssolutions.com',
    'summary': 'Purchase Order',
    'description': """ Purchase order sequence """,
    'depends': [
        'purchase','base',
    ],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}