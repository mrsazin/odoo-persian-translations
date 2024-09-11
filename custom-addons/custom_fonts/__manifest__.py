 # -*- coding: utf-8 -*-
{
    'name': "custom fonts report",

    'summary': """
        change defult font to nice persian font""",

    'description': """
        Change the defult persian font of the all interfaces with a beautiful one preferred by the Persian user
 ,
    """,
    'author': "Azar",
    "category": "Localization/Iran",
    "version": "1.0.1",
    'depends': ['base'],
    'license': 'LGPL-3',
    'assets': {
        'web.report_assets_common': [
            'custom_font/static/src/scss/persiangont.scss',
        ],
    },
    "installable": True,
    "auto_install": False,
}
