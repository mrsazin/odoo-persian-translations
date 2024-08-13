# -*- coding: utf-8 -*-
{
    'name' : 'SHP Components',
    'version' : '1.0',
    'summary': 'SHP Components',
    'sequence': -1,
    'description': """SHP Components""",
    'category': 'SHP',
    'depends' : ['web', 'sale', 'point_of_sale'],
    'data': [
        'views/point_of_sale_dashboard.xml',
        'views/report_saledetails_custom.xml',
        'views/point_of_sale_report.xml',
        'wizard/pos_details.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale._assets_core': [
          
        ],
        'shp._assets_core': [
          
        ],
        'web._assets_core': [
          
        ],
        'point_of_sale.assets_frontend': [
          
        ],
        'web.assets_backend': [
            'shp/static/src/components/shpDateTime/shpDateTime_field.js',
            'shp/static/src/components/shpDateTime/shpDateTime_field.xml',
          
        ],
        'point_of_sale.assets_backend': [
            'shp/static/src/lib/farvardin.js',
            'shp/static/src/lib/jalali-moment.browser.js',
            'shp/static/src/lib/convert-date-to-persian-in-javascript.js',
        ],
        'web._assets_pos': [
          
        ],
        'web.assets_common': [
          
        ],
        'point_of_sale._assets_pos': [
            'shp/static/src/order_receipt.js',
            'shp/static/src/order_receipt.xml',
            'shp/static/src/receipt_header.js',
            'shp/static/src/payment_screen.js',
            'shp/static/src/receipt_header.xml',
            'shp/static/src/orderline.xml',
            'shp/static/src/order_widget.xml',
            'shp/static/src/receipt.scss',
            'shp/static/src/pos_app.scss',
            'shp/static/src/payment_status.scss',
            'shp/static/src/lib/shpdates.js',
            'shp/static/src/lib/models.js',
            'shp/static/src/debug_widget.js',
            'shp/static/src/error_traceback_popup.js',
            'shp/static/src/debug_widget.js',
            'shp/static/src/ticket_screen.js',
            'shp/static/src/sale_details_button.js',
            'shp/static/src/lib/jalali-moment.browser.js',
            
            
            
            
            
            # 'web/static/lib/luxon/luxon.js',
            # 'shp/static/src/lib/jalali-moment.browser.js',
            
            # 'shp/static/src/lib/shpluxon.js',
            
        ],
        
        
    },
}