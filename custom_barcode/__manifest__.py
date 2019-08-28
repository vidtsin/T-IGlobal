# -*- encoding: utf-8 -*-
{
    'name': 'Custom Barcodes',
    'version': '12.0',
    'author': 'PPTS [India] Pvt.Ltd.',
    'category': 'Barcodes',
    'description': """This module allows you to scan the location of a product from a stock and navigates to it.
    Scans the barcode related to a stock , product and location and navigates to their form view
    """,
    'summary':"Scans the barcodes and views it's related form.",
    'depends': ['base', 'stock_barcode', 'barcodes', 'purchase', 'sale', 'product', 'stock', 'stock_barcode_mobile', 'web_mobile'],
    'qweb': ['static/xml/scan_location_barcode.xml', 'static/xml/location_mobile_barcode.xml','static/xml/barcode_menu.xml'],
    'data': [
        'views/scan_location_template.xml',
        'views/scan_location_barcode.xml',
        'views/custom_barcode.xml',
        'wizard/scan_location_barcode.xml',
        ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
