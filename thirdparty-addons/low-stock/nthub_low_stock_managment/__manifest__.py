# -*- coding: utf-8 -*-
{
    'name': "POS Low Stock Alert",
    'version': '17.0',
    'summary': """Product Low Stock Alert Display in Point of Sale and 
    Product Views""",
    "category": 'Warehouse,Point of Sale',
    'description': """Module adds functionality to display product stock 
    alerts in the point of sale interface, indicating low stock levels for 
    products and also in the product variant kanban and list view.""",
    'author': 'Neoteric Hub',
    'company': 'Neoteric Hub',
    'live_test_url': '',
    'price': 0,
    'currency': 'USD',
    'website': 'https://www.neoterichub.com',
    'depends': ['stock', 'point_of_sale'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_product_views.xml',
    ],
    'assets': {
        'web.assets_backend': [

        ],
        'point_of_sale._assets_pos': [
            'nthub_low_stock_managment/static/src/css/display_stock.css',
            'nthub_low_stock_managment/static/src/js/PaymentScreen.js',
            'nthub_low_stock_managment/static/src/xml/product_item_template.xml',
        ],
    },
    'images': ['static/description/banner.gif'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
