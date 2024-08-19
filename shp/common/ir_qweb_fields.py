# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class DateConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.date'

    @api.model
    def get_available_options(self):
        options = super(DateConverter, self).get_available_options()
        options.update(
            format=dict(type='string', string=_('Date format'))
        )
        return options

    @api.model
    def value_to_html(self, value, options):
        return value
