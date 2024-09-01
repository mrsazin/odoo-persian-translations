 # -*- coding: utf-8 -*-
{
    'name': "Persian font",

    'summary': """
        change defult font to nice persian font""",

    'description': """
        Change the defult persian font of the all interfaces with a beautiful one preferred by the Persian user
 ,
    """,
    'author': "Fadoo",
    'website': "http://fadoo.com",
    "category": "Localization/Iran",
    "version": "1.0.1",
    'depends': ['web'],
    'license': 'AGPL-3',
    'assets': {
        'web._assets_primary_variables': [
            'l10n_ir_fonts/static/src/scss/persianfont.scss',
        ],
        'web.assets_backend': [
            'l10n_ir_fonts/static/src/css/pos_style.css',
            'l10n_ir_fonts/static/src/css/web_style.css',
        ],
        'web.report_assets_common': [
            'l10n_ir_fonts/static/src/css/pdf_style.css',
        ],
        'web.report_assets_pdf': [
            'l10n_ir_fonts/static/src/css/pdf_style.css',
        ],
        'account_reports.assets_financial_report': [
            'l10n_ir_fonts/static/src/css/pdf_style.css',
        ],
    },
    "installable": True,
    "auto_install": False,
}
