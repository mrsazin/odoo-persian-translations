# -*- coding: utf-8 -*-
import logging

from odoo import fields, http, _
from odoo.http import request
from odoo.osv.expression import AND
from odoo.tools import format_amount
from odoo.addons.account.controllers.portal import PortalAccount
from datetime import timedelta, datetime

_logger = logging.getLogger(__name__)


class PosController(PortalAccount):
    _inherit = 'PosController' 

    @http.route('/pos/sale_details_report', type='http', auth='user')
    def print_sale_details(self, date_start=False, date_stop=False, **kw):
        print("main")
        r = request.env['report.point_of_sale.report_saledetails']
        pdf, _ = request.env['ir.actions.report'].with_context(date_start=date_start, date_stop=date_stop)._render_qweb_pdf('point_of_sale.sale_details_report_inherit', r)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route(['/pos/ticket'], type='http', auth="public", website=True, sitemap=False)
    def invoice_request_screen(self, **kwargs):
        errors = {}
        form_values = {}
        if request.httprequest.method == 'POST':
            for field in ['pos_reference', 'date_order', 'ticket_code']:
                if not kwargs.get(field):
                    errors[field] = " "
                else:
                    form_values[field] = kwargs.get(field)

            if errors:
                errors['generic'] = _("Please fill all the required fields.")
            elif len(form_values['pos_reference']) < 14:
                errors['pos_reference'] = _("The Ticket Number should be at least 14 characters long.")
            else:
                date_order = fields.DateTime.to_datetime(*[int(i) for i in form_values['date_order'].split('-')])
                order = request.env['pos.order'].sudo().search([
                    ('pos_reference', '=like', '%' + form_values['pos_reference'].replace('%', r'\%').replace('_', r'\_')),
                    ('date_order', '>=', date_order),
                    ('date_order', '<', date_order + timedelta(days=1)),
                    ('ticket_code', '=', form_values['ticket_code']),
                ], limit=1)
                if order:
                    return request.redirect('/pos/ticket/validate?access_token=%s' % (order.access_token))
                else:
                    errors['generic'] = _("No sale order found.")

        return request.render("point_of_sale.ticket_request_with_code", {
            'errors': errors,
            'banner_error': " ".join(errors.values()),
            'form_values': form_values,
        })