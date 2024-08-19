# -*- coding: utf-8 -*-

from datetime import datetime
from khayyam import JalaliDate, JalaliDatetime, TehranTimezone
import pytz
from odoo import api, fields, models
# import odoo.addons.shp.common.fields as myfields


class PosConfig(models.Model):
    _inherit = 'pos.config'       

    @api.depends('session_ids')
    def _compute_last_session(self):
        PosSession = self.env['pos.session']
        for pos_config in self:
            session = PosSession.search_read(
                [('config_id', '=', pos_config.id), ('state', '=', 'closed')],
                ['cash_register_balance_end_real', 'stop_at'],
                order="stop_at desc", limit=1)
            if session:
                # timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
                last_session_date = fields.Datetime.to_datetime(str((session[0]['stop_at']))[:10]).astimezone(TehranTimezone()).date()

                pos_config.last_session_closing_date = last_session_date
                pos_config.last_session_closing_cash = session[0]['cash_register_balance_end_real']
            else:
                pos_config.last_session_closing_cash = 0
                pos_config.last_session_closing_date = False
    
    @api.depends('session_ids')
    def _compute_current_session_user(self):
        for pos_config in self:
            session = pos_config.session_ids.filtered(lambda s: s.state in ['opening_control', 'opened', 'closing_control'] and not s.rescue)
            if session:
                pos_config.pos_session_username = session[0].user_id.sudo().name
                pos_config.pos_session_state = session[0].state
                pos_config.pos_session_duration = (
                    fields.Datetime.now() - fields.Datetime.to_datetime(session[0].start_at)
                ).days if session[0].start_at else 0
                pos_config.current_user_id = session[0].user_id
            else:
                pos_config.pos_session_username = False
                pos_config.pos_session_state = False
                pos_config.pos_session_duration = 0
                pos_config.current_user_id = False

    last_session_closing_date = fields.Date(compute='_compute_last_session')
    