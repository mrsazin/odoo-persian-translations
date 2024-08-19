# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pytz
from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.shp.common.fields as myfields


class PosDetails(models.TransientModel):
    _inherit = 'pos.details.wizard'

    def _default_start_date(self):
        """ Find the earliest start_date of the latests sessions """
        # restrict to configs available to the user
        config_ids = self.env['pos.config'].search([]).ids
        # exclude configs has not been opened for 2 days
        self.env.cr.execute("""
            SELECT
            max(start_at) as start,
            config_id
            FROM pos_session
            WHERE config_id = ANY(%s)
            AND start_at::TIMESTAMP > %s
            GROUP BY config_id 
        """, (config_ids, fields.Datetime.to_string(fields.Datetime.now() - timedelta(days=2))))
        latest_start_dates = [res['start'] for res in self.env.cr.dictfetchall()]
        # earliest of the latest sessions
        return latest_start_dates and min(latest_start_dates) or fields.Datetime.now()

    start_date = fields.Char(required=True, default=_default_start_date)
    end_date = fields.Char(required=True, default=fields.Datetime.now())
    pos_config_ids = fields.Many2many('pos.config', 'pos_detail_configs',
        default=lambda s: s.env['pos.config'].search([]))

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date
        if len(self.start_date) > 19:
            self.start_date = self.start_date[:19]
        if len(self.end_date) > 19:
            self.end_date = self.end_date[:19]

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            self.start_date = self.end_date
        if len(self.start_date) > 19:
            self.start_date = self.start_date[:19]
        if len(self.end_date) > 19:
            self.end_date = self.end_date[:19]

    def generate_report(self): 
        data = {'date_start': self.start_date, 'date_stop': self.end_date, 'config_ids': self.pos_config_ids.ids}
        return self.env.ref('point_of_sale.sale_details_report').report_action([], data=data)
