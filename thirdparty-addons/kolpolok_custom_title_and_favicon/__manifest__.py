# -*- coding: utf-8 -*-
################################################################################
#
#    Kolpolok Ltd. (https://www.kolpolok.com)
#    Author: Kolpolok (<https://www.kolpolok.com>)
#
################################################################################

{
    'name': 'Custom Title and Favicon',
    'version': '17.0.0.0',
    'sequence': 1,
    'summary': """
        This module customizes title and favicon logo, boosting brand recognition and success.
    """,
    'description': "Custom Title & Favicon",
    'author': 'Kolpolok',
    'maintainer': 'Kolpolok',
    'price': '0.0',
    'currency': 'USD',
    'website': 'https://www.kolpoloktechnologies.com/',
    'license': 'LGPL-3',
    'images': [
        'static/description/banner.gif'
    ],
    'depends': [
        'web'
    ],
    'data': [
        'data/demo_data.xml',
        'views/favicon.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kolpolok_custom_title_and_favicon/static/src/js/favicon.js',
        ],
    },
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
        
    ],
}
