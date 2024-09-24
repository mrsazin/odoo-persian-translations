# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custome Branding',
    'summary': 'Customizes the logos and branding of Odoo' ,
    'category': 'Customization',
    'version': '1.0',
    'author':'Azar Nazari (azar.nazari@gmail.com)',
    'description': """
RG Branding
========================

This module Changes all Odoo's logos of the Odoo Web Client.
""",
    'depends': ['web'],
    'data': [ 
        '/views/webclient_templates.xml'
             ],
    'assets': {
        'web.assets_backend': [
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
            'custom_branding/static/img',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
