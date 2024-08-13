# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import secrets
from collections import defaultdict
from datetime import timedelta
from itertools import groupby
from operator import itemgetter
from traceback import format_exception
from typing import Optional

import json
import logging

from odoo import api, fields, models, _, Command
from odoo.addons.base.models.ir_qweb_fields import Markup, escape, nl2br
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.osv.expression import AND
from odoo.service.common import exp_version
from odoo.tools import float_is_zero, float_compare, convert
from odoo.tools.misc import str2bool
import odoo.addons.shp.common.fields as myfields
from khayyam import JalaliDate

_logger = logging.getLogger(__name__)

class PosSession(models.Model):    
    _inherit = 'pos.session'
    
    start_at = myfields.Datetime(string='Opening Date', readonly=True)
    stop_at = myfields.Datetime(string='Closing Date', readonly=True, copy=False)

    
    @api.constrains('start_at')
    def _check_start_date(self):
        for record in self:
            company = record.config_id.journal_id.company_id
            start_date = myfields.Date.to_date(record.start_at)
            if (company.period_lock_date and start_date <= JalaliDate(company.period_lock_date)) or (start_date.todate() <= company._get_user_fiscal_lock_date()):
                raise ValidationError(_("You cannot create a session before the accounting lock date."))

    def action_pos_session_open(self):
        # we only open sessions that haven't already been opened
        for session in self.filtered(lambda session: session.state == 'opening_control'):
            values = {}
            if not session.start_at:
                values['start_at'] = myfields.Datetime.now()
            if session.config_id.cash_control and not session.rescue:
                last_session = self.search([('config_id', '=', session.config_id.id), ('id', '!=', session.id)], limit=1)
                session.cash_register_balance_start = last_session.cash_register_balance_end_real  # defaults to 0 if lastsession is empty
            else:
                values['state'] = 'opened'
            session.write(values)
        return True

    @api.model
    def _alert_old_session(self):
        # If the session is open for more then one week,
        # log a next activity to close the session.
        sessions = self.sudo().search([('start_at', '<=', (myfields.datetime.now() - timedelta(days=7))), ('state', '!=', 'closed')])
        for session in sessions:
            if self.env['mail.activity'].search_count([('res_id', '=', session.id), ('res_model', '=', 'pos.session')]) == 0:
                session.activity_schedule(
                    'point_of_sale.mail_activity_old_session',
                    user_id=session.user_id.id,
                    note=_(
                        "Your PoS Session is open since %(date)s, we advise you to close it and to create a new one.",
                        date=session.start_at,
                    )
                )
    
    def action_pos_session_closing_control(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        bank_payment_method_diffs = bank_payment_method_diffs or {}
        for session in self:
            if any(order.state == 'draft' for order in session.order_ids):
                raise UserError(_("You cannot close the POS when orders are still in draft"))
            if session.state == 'closed':
                raise UserError(_('This session is already closed.'))
            stop_at = self.stop_at or myfields.Datetime.now()
            session.write({'state': 'closing_control', 'stop_at': stop_at})
            if not session.config_id.cash_control:
                return session.action_pos_session_close(balancing_account, amount_to_balance, bank_payment_method_diffs)
            # If the session is in rescue, we only compute the payments in the cash register
            # It is not yet possible to close a rescue session through the front end, see `close_session_from_ui`
            if session.rescue and session.config_id.cash_control:
                default_cash_payment_method_id = self.payment_method_ids.filtered(lambda pm: pm.type == 'cash')[0]
                orders = self._get_closed_orders()
                total_cash = sum(
                    orders.payment_ids.filtered(lambda p: p.payment_method_id == default_cash_payment_method_id).mapped('amount')
                ) + self.cash_register_balance_start

                session.cash_register_balance_end_real = total_cash

            return session.action_pos_session_validate(balancing_account, amount_to_balance, bank_payment_method_diffs)

    def update_closing_control_state_session(self, notes):
        # Prevent closing the session again if it was already closed
        if self.state == 'closed':
            raise UserError(_('This session is already closed.'))
        # Prevent the session to be opened again.
        self.write({'state': 'closing_control', 'stop_at': myfields.Datetime.now(), 'closing_notes': notes})
        self._post_cash_details_message('Closing', self.cash_register_difference, notes)