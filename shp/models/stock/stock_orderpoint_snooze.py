# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.date_utils import add
import odoo.addons.shp.common.fields as myfields

class StockOrderpointSnooze(models.TransientModel):
    _inherit = 'stock.orderpoint.snooze'

    orderpoint_ids = fields.Many2many('stock.warehouse.orderpoint')
    predefined_date = fields.Selection([
        ('day', '1 Day'),
        ('week', '1 Week'),
        ('month', '1 Month'),
        ('custom', 'Custom')
    ], string='Snooze for', default='day')
    snoozed_until = fields.Date('Snooze Date')

    @api.onchange('predefined_date')
    def _onchange_predefined_date(self):
        today = fields.Date.context_today(self)
        if self.predefined_date == 'day':
            self.snoozed_until = add(today, days=1)
        elif self.predefined_date == 'week':
            self.snoozed_until = add(today, weeks=1)
        elif self.predefined_date == 'month':
            self.snoozed_until = add(today, months=1)

    def action_snooze(self):
        self.orderpoint_ids.write({
            'snoozed_until': self.snoozed_until
        })
