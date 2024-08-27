# See LICENSE file for full copyright and licensing details.

from ast import literal_eval
from odoo import api, fields, models, sql_db, _, tools, Command
from odoo.tools.misc import formatLang, get_lang, format_amount
from odoo.exceptions import ValidationError, RedirectWarning
from odoo.tools.mimetypes import guess_mimetype
from datetime import datetime
from odoo.tools import pycompat
from odoo.exceptions import UserError
import html2text
from odoo.tools import is_html_empty
from odoo.addons.mail.tools.parser import parse_res_ids
from ..klikapi import texttohtml
import requests
import json
import ast
import base64
import threading
import time
import logging

_logger = logging.getLogger(__name__)


try:
    import phonenumbers
    from phonenumbers.phonenumberutil import region_code_for_country_code
    _sms_phonenumbers_lib_imported = True

except ImportError:
    _sms_phonenumbers_lib_imported = False
    _logger.info(
        "The `phonenumbers` Python module is not available. "
        "Phone number validation will be skipped. "
        "Try `pip3 install phonenumbers` to install it."
    )
    

# def _reopen(self, res_id, model, context=None):
#     # save original model in context, because selecting the list of available
#     # templates requires a model in context
#     context = dict(context or {}, default_model=model)
#     action = {'type': 'ir.actions.act_window',
#             'view_mode': 'form',
#             'res_id': res_id,
#             'res_model': self._name,
#             'target': 'new',
#             'context': context,
#             }
#     print ('===action==',action)
#     return action

class WhatsappComposeMessage(models.TransientModel):
    _name = 'whatsapp.compose.message'
    _description = "Whatsapp Message"

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        context = self.env.context
        if context.get('active_model'):
            print ('=context==',context)
            result['model'] = context['active_model']
            # result['subject'] = context['subject']
            #result['model'] = context['active_model']
            #if 'res_id' in fields and 'res_id' not in result:
            # if context.get('active_ids'):
            #     result['res_ids'] = context.get('active_ids')
            # else:
            #     result['res_id'] = context.get('active_id')
            if context.get('active_ids') or context.get('active_id'):
                result['res_ids'] = context.get('active_ids') or [context.get('active_id')]
            #result['res_ids'] = context.get('active_ids') or [context.get('active_id')]
            partners = self.env['res.partner']
            if result['model'] and context['active_model'] and result['model'] == 'res.partner':
                partners = self.env[result['model']].browse(result['res_ids'])
                result['model'] = result['model'] or 'res.partner'
                result['partner_ids'] = [(6, 0, partners.ids)]
            else:
                partners = self.env[result['model']].browse(result['res_ids']).mapped('partner_id')
                result['partner_ids'] = [(6, 0, partners.ids)]
            wa_template_id = self.env['mail.template']._find_default_for_template(result['model'])
            print ('==wa_template_id=',wa_template_id,result.get('wa_template_id'))
            if wa_template_id and not result.get('wa_template_id'):
                result['template_id'] = wa_template_id.id
            elif not wa_template_id and not result.get('wa_template_id'):
                action = self.env.ref('mail.action_email_template_tree_all')
                raise RedirectWarning(_("No template available for this model"), action.id, _("View Templates"))
                # if self.env.user.has_group('whatsapp.group_whatsapp_admin'):
                #     action = self.env.ref('mail.action_email_template_tree_all')
                #     raise RedirectWarning(_("No template available for this model"), action.id, _("View Templates"))
                # else:
                #     raise ValidationError(_("No template available for this model"))
        # if context.get('active_ids') or context.get('active_id'):
        #     result['res_ids'] = context.get('active_ids') or [context.get('active_id')]
        if context.get('active_ids') and len(context['active_ids']) > 1:
            result['batch_mode'] = True
        return result

    @api.model
    def _get_composition_mode_selection(self):
        return [('comment', 'Post on a document'),
                ('mass_mail', 'Whatsapp Mass Mailing'),
                ('mass_post', 'Post on Multiple Documents')]
        
    #invoice_ids = fields.Many2many('account.invoice', string='Invoice')
    composition_mode = fields.Selection(selection=_get_composition_mode_selection, string='Composition mode', default='comment')
    composition_batch = fields.Boolean(
        'Batch composition', compute='_compute_composition_batch')  # more than 1 record (raw source)
    partner_ids = fields.Many2many('res.partner', string='Contacts')
    subject = fields.Char('Subject')
    # message = fields.Text()
    message = fields.Text(
        'Contents',
        # render_engine='qweb', render_options={'post_process': True},
        # sanitize_style=True,
        compute='_compute_body', readonly=False, store=True)
    batch_mode = fields.Boolean("Is Multiple Records")
    #message_html = fields.Html()
    res_domain = fields.Text('Active domain')
    res_id = fields.Integer('Record Document ID', required=False)
    res_ids = fields.Char('Document IDs', required=False)
    model = fields.Char('Object')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'whatsapp_compose_message_ir_attachments_rel',
        'wizard_id', 'attachment_id', string='Attachments',
        compute='_compute_attachment_ids', readonly=False, store=True)
    #url_link = fields.Char('Url')
    location = fields.Boolean('Location')
    partner_address_id = fields.Many2one('res.partner', string='Address')
    lat = fields.Float('Lat')
    long = fields.Float('Long')
    type = fields.Selection([('contact', 'Contacts'),('group', 'Groups')], default='group')
    whatsapp_type = fields.Selection([('post', 'Post'),('get', 'Get')], default='post')
    template_id = fields.Many2one(
        'mail.template', 'Use template', index=True,
        domain="[('model', '=', model), '|', ('user_id','=', False), ('user_id', '=', uid)]"
        )

    def _get_active_records(self):
        self.ensure_one()
        return self.env[self.res_model].browse(literal_eval(self.res_ids))

    @api.depends('res_ids')
    def _compute_composition_batch(self):
        """ Determine if batch mode is activated:

          * using res_domain: always batch (even if result is singleton at a
            given time, it is user and time dependent, hence batch);
          * res_ids: if more than one item in the list (void and singleton are
            not batch);
        """
        for composer in self:
            if composer.res_domain:
                composer.composition_batch = True
                continue
            res_ids = composer._evaluate_res_ids()
            composer.composition_batch = len(res_ids) > 1 if res_ids else False

    # @api.onchange('template_id')
    # def _onchange_template_id_wrapper(self):
    #     self.ensure_one()
    #     # records = self._get_active_records()
    #     # res_id = self._context.get('active_id') or 1
    #     print ('==_onchange_template_id_wrapper==',self.template_id.id, self.composition_mode, self.model, self.res_id, self.res_ids)
    #     if self.res_ids:
    #         res_id = ast.literal_eval(self.res_ids)[0]
    #         values = self._onchange_template_id(self.template_id.id, self.composition_mode, self.model, res_id)['value']
    #         for fname, value in values.items():
    #             setattr(self, fname, value)

    
    # def _onchange_template_id(self, template_id, composition_mode, model, res_id):
    #     """ - mass_mailing: we cannot render, so return the template values
    #         - normal mode: return rendered values
    #         /!\ for x2many field, this onchange return command instead of ids
    #     """
    #     if template_id and composition_mode == 'mass_mail':
    #         template = self.env['mail.template'].browse(template_id)
    #         values = dict(
    #             (field, template[field])
    #             for field in ['subject', 'body_html',
    #                         #   'email_from',
    #                           'reply_to',
    #                           'mail_server_id']
    #             if template[field]
    #         )
    #         if template.sudo().attachment_ids:
    #             values['attachment_ids'] = [att.id for att in template.sudo().attachment_ids]
    #         if template.mail_server_id:
    #             values['mail_server_id'] = template.mail_server_id.id
    #     elif template_id:
    #         values = self.generate_email_for_composer(
    #             template_id, [res_id],
    #             ['subject', 'body_html',
    #             #  'email_from',
    #              'email_cc', 'email_to', 'partner_to', 'reply_to',
    #              'attachment_ids', 'report_template_ids', 'mail_server_id'
    #             ]
    #         )[res_id]
    #         # transform attachments into attachment_ids; not attached to the document because this will
    #         # be done further in the posting process, allowing to clean database if email not send
    #         attachment_ids = []
    #         Attachment = self.env['ir.attachment'].sudo()
    #         for attach_fname, attach_datas in values.pop('attachments', []):
    #             data_attach = {
    #                 'name': attach_fname,
    #                 'datas': attach_datas,
    #                 'res_model': 'whatsapp.compose.message',
    #                 'res_id': res_id,
    #                 'type': 'binary',  # override default_type from context, possibly meant for another model!
    #             }
    #             print ('==attach_fname==',attach_fname,res_id)
    #             attachment_ids.append(Attachment.create(data_attach).id)
    #         if values.get('attachment_ids', []) or attachment_ids:
    #             values['attachment_ids'] = [Command.set(values.get('attachment_ids', []) + attachment_ids)]
    #     else:
    #         default_values = self.with_context(
    #             default_composition_mode=composition_mode,
    #             default_model=model,
    #             default_res_id=res_id
    #         ).default_get(['composition_mode', 'model', 'res_id', 'parent_id',
    #                        'subject', 'body',
    #                     #    'email_from',
    #                        'partner_ids', 'reply_to',
    #                        'attachment_ids', 'mail_server_id'
    #                       ])
    #         values = dict(
    #             (key, default_values[key])
    #             for key in ['subject', 'body',
    #                         # 'email_from',
    #                         'partner_ids', 'reply_to',
    #                         'attachment_ids', 'mail_server_id'
    #                        ] if key in default_values)

    #     if values.get('body_html'):
    #         values['body'] = values.pop('body_html')

    #     # This onchange should return command instead of ids for x2many field.
    #     values = self.sudo()._convert_to_write(values)

    #     return {'value': values}
    

    @api.depends('composition_mode', 'model', 'res_ids',
                 'template_id')
    def _compute_body(self):
        """ Computation is coming either from template, either reset. When
        having a template with a value set, copy it (in batch mode) or render
        it (in monorecord comment mode) on the composer. When removing the
        template, reset it. """
        for composer in self:
            if composer.template_id:
                composer.message = html2text.html2text(self.template_id.body_html) if self.template_id.body_html else 'Sample Message'
                # composer._set_value_from_template('body_html', 'message')
            if not composer.template_id:
                composer.message = False

    @api.depends('composition_mode', 'model', 'res_ids', 'template_id')
    def _compute_attachment_ids(self):
        """ Computation is based on template and composition mode. In monorecord
        comment mode, template is used to generate attachments based on both
        attachment_ids of template, and reports coming from report_template_ids.
        Those are generated based on the current record to display. As template
        generation returns a list of tuples, new attachments are created on
        the fly during the compute.

        In batch or email mode, only attachment_ids from template are used on
        the composer. Reports will be generated at sending time.

        When template is removed, attachments are reset. """
        for composer in self:
            res_ids = composer._evaluate_res_ids() or [0]
            if (composer.template_id.attachment_ids and
                (composer.composition_mode == 'mass_mail' or composer.composition_batch)):
                composer.attachment_ids = composer.template_id.attachment_ids
            elif composer.template_id and composer.composition_mode == 'comment' and len(res_ids) == 1:
                rendered_values = composer._generate_template_for_composer(
                    res_ids,
                    ('attachment_ids', 'attachments'),
                )[res_ids[0]]
                attachment_ids = rendered_values.get('attachment_ids') or []
                # transform attachments into attachment_ids; not attached to the
                # document because this will be done further in the posting
                # process, allowing to clean database if email not send
                if rendered_values.get('attachments'):
                    attachment_ids += self.env['ir.attachment'].create([
                        {'name': attach_fname,
                         'datas': attach_datas,
                         'res_model': 'whatsapp.compose.message',
                         'res_id': 0,
                         'type': 'binary',    # override default_type from context, possibly meant for another model!
                        } for attach_fname, attach_datas in rendered_values.pop('attachments')
                    ]).ids
                if attachment_ids:
                    composer.attachment_ids = attachment_ids
            elif not composer.template_id:
                composer.attachment_ids = False

    def _evaluate_res_ids(self):
        """ Parse composer res_ids, which can be: an already valid list or
        tuple (generally in code), a list or tuple as a string (coming from
        actions). Void strings / missing values are evaluated as an empty list.

        Note that 'active_ids' context key is supported at this point as mailing
        on big ID list would create issues if stored in database.

        Another context key 'composer_force_res_ids' is temporarily supported
        to ease support of accounting wizard, while waiting to implement a
        proper solution to language management.

        :return: a list of IDs (empty list in case of falsy strings)"""
        self.ensure_one()
        return parse_res_ids(
            self.env.context.get('composer_force_res_ids') or
            self.res_ids or
            self.env.context.get('active_ids')
        ) or []

    # def _set_value_from_template(self, template_fname, composer_fname=False):
    #     """ Set composer value from its template counterpart. In monorecord
    #     comment mode, we get directly the rendered value, giving the real
    #     value to the user. Otherwise we get the raw (unrendered) value from
    #     template, as it will be rendered at send time (for mass mail, whatever
    #     the number of contextual records to mail) or before posting on records
    #     (for comment in batch).

    #     :param str template_fname: name of field on template model, used to
    #       fetch the value (and maybe render it);
    #     :param str composer_fname: name of field on composer model, when field
    #       names do not match (e.g. body_html on template used to populate body
    #       on composer);
    #     """
    #     self.ensure_one()
    #     composer_fname = composer_fname or template_fname

    #     # fetch template value, check if void
    #     template_value = self.template_id[template_fname] if self.template_id else False
    #     if template_value and template_fname == 'body_html':
    #         template_value = template_value if not is_html_empty(template_value) else False
    #         template_value = html2text.html2text(template_value)
    #     if template_value:
    #         if self.composition_mode == 'comment' and not self.composition_batch:
    #             res_ids = self._evaluate_res_ids()
    #             rendering_res_ids = res_ids or [0]
    #             self[composer_fname] = self.template_id._generate_template(
    #                 rendering_res_ids,
    #                 {template_fname},
    #             )[rendering_res_ids[0]][template_fname]
    #         else:
    #             self[composer_fname] = self.template_id[template_fname]
    #     # html2text.html2text(res_id_values.pop('body_html', ''))
    #     print ('==compose==',html2text.html2text(self[composer_fname]),)
    #     return html2text.html2text(self[composer_fname])

    def _generate_template_for_composer(self, res_ids, render_fields,
                                        find_or_create_partners=True):
        """ Generate values based on template and relevant values for the
        mail.compose.message wizard.

        :param list res_ids: list of record IDs on which template is rendered;
        :param list render_fields: list of fields to render on template;
        :param boolean find_or_create_partners: transform emails into partners
          (see ``Template._generate_template_recipients``);

        :returns: a dict containing all asked fields for each record ID given by
          res_ids. Note that

          * 'body' comes from template 'body_html' generation;
          * 'attachments' is an additional key coming with 'attachment_ids' due
            to report generation (in the format [(report_name, data)] where data
            is base64 encoded);
          * 'partner_ids' is returned due to recipients generation that gives
            partner ids coming from default computation as well as from email
            to partner convert (see ``find_or_create_partners``);
        """
        self.ensure_one()

        # some fields behave / are named differently on template model
        mapping = {
            'attachments': 'report_template_ids',
            'message': 'body_html',
            'partner_ids': 'partner_to',
        }
        template_fields = {mapping.get(fname, fname) for fname in render_fields}
        template_values = self.template_id._generate_template(
            res_ids,
            template_fields,
            find_or_create_partners=True
        )
        # res_id_values = dict((field, template_values[res_id][field]) for field in returned_fields if template_values[res_id].get(field))
        # res_id_values['message'] = html2text.html2text(res_id_values.pop('body_html', ''))
        exclusion_list = ('email_cc', 'email_to') if find_or_create_partners else ()
        mapping = {'body_html': 'message'}
        render_results = {}
        for res_id in res_ids:
            render_results[res_id] = {
                mapping.get(fname, fname): value
                for fname, value in template_values[res_id].items()
                if fname not in exclusion_list and value
            }
            # print ('===s==',render_results[res_id])
        return render_results

    # def action_save_as_template(self):
    #     """ hit save as template button: current form value will be a new
    #         template attached to the current document. """
    #     for record in self:
    #         model = self.env['ir.model']._get(record.model or 'mail.message')
    #         model_name = model.name or ''
    #         template_name = "%s: %s" % (model_name, tools.ustr(record.subject))
    #         values = {
    #             'name': template_name,
    #             'subject': record.subject or False,
    #             'body_html': record.body or False,
    #             'model_id': model.id or False,
    #             'use_default_to': True,
    #         }
    #         template = self.env['mail.template'].create(values)

    #         if record.attachment_ids:
    #             attachments = self.env['ir.attachment'].sudo().browse(record.attachment_ids.ids).filtered(
    #                 lambda a: a.res_model == 'mail.compose.message' and a.create_uid.id == self._uid)
    #             if attachments:
    #                 attachments.write({'res_model': template._name, 'res_id': template.id})
    #             template.attachment_ids |= record.attachment_ids

    #         # generate the saved template
    #         record.write({'template_id': template.id})
    #         record._onchange_template_id_wrapper()
    #         return _reopen(self, record.id, record.model, context=self._context)
    
    # @api.onchange('template_id')
    # def onchange_template_id_wrapper(self):
    #     self.ensure_one()
    #     res_id = self._context.get('active_id') or 1
    #     values = self.onchange_template_id(self.template_id.id, self.model, res_id)['value']
    #     for fname, value in values.items():
    #         setattr(self, fname, value)
    
    # def onchange_template_id(self, template_id, model, res_id):
    #     """ - mass_mailing: we cannot render, so return the template values
    #         - normal mode: return rendered values
    #         /!\ for x2many field, this onchange return command instead of ids
    #     """
    #     if template_id:
    #         values = self.generate_email_for_composer(template_id, [res_id])[res_id]
    #     else:
    #         default_values = self.with_context(default_model=model, default_res_id=res_id).default_get(['model', 'res_id', 'partner_ids', 'message', 'attachment_ids'])
    #         values = dict((key, default_values[key]) for key in ['subject', 'body', 'partner_ids', 'email_from', 'reply_to', 'attachment_ids', 'mail_server_id'] if key in default_values)
    #     # This onchange should return command instead of ids for x2many field.
    #     # ORM handle the assignation of command list on new onchange (api.v8),
    #     # this force the complete replacement of x2many field with
    #     # command and is compatible with onchange api.v7
    #     values = self._convert_to_write(values)
    #     return {'value': values}
    
    # @api.model
    # def generate_email_for_composer(self, template_id, res_ids, fields=None):
    #     """ Call email_template.generate_email(), get fields relevant for
    #         mail.compose.message, transform email_cc and email_to into partner_ids """
    #     multi_mode = True
    #     if isinstance(res_ids, pycompat.integer_types):
    #         multi_mode = False
    #         res_ids = [res_ids]

    #     if fields is None:
    #         fields = ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc',  'reply_to', 'attachment_ids', 'mail_server_id']
    #     returned_fields = fields + ['partner_ids', 'attachments']
    #     values = dict.fromkeys(res_ids, False)
    #     print ('===res_ids==',values)
    #     template_values = self.env['mail.template'].with_context(tpl_partners_only=True).browse(template_id).generate_email(res_ids, fields=fields)
    #     for res_id in res_ids:
    #         res_id_values = dict((field, template_values[res_id][field]) for field in returned_fields if template_values[res_id].get(field))
    #         res_id_values['message'] = html2text.html2text(res_id_values.pop('body_html', ''))
    #         values[res_id] = res_id_values

    #     return multi_mode and values or values[res_ids[0]]
    
    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        """ Call email_template.generate_email(), get fields relevant for
            whatsapp.compose.message, transform email_cc and email_to into partner_ids """
        multi_mode = True
        if isinstance(res_ids, int):
            multi_mode = False
            res_ids = [res_ids]

        if fields is None:
            fields = ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc',  'reply_to', 'attachment_ids', 'mail_server_id']
        returned_fields = fields + ['partner_ids', 'attachments']
        values = dict.fromkeys(res_ids, False)
        # print ('==template_values=11=',fields)
        template_values = self.env['mail.template'].with_context(tpl_partners_only=True).browse(template_id)._generate_template(res_ids, render_fields=fields)
        # print ('==template_values==',template_values)
        for res_id in res_ids:
            res_id_values = dict((field, template_values[res_id][field]) for field in returned_fields if template_values[res_id].get(field))
            res_id_values['message'] = html2text.html2text(res_id_values.pop('body_html', ''))
            values[res_id] = res_id_values
        # print ('==template_values=22=',fields)
        return multi_mode and values or values[res_ids[0]]
    
    def format_amount(self, amount, currency):
        fmt = "%.{0}f".format(currency.decimal_places)
        lang = self.env['res.lang']._lang_get(self.env.context.get('lang') or 'en_US')
 
        formatted_amount = lang.format(fmt, currency.round(amount), grouping=True, monetary=True)\
            .replace(r' ', u'\N{NO-BREAK SPACE}').replace(r'-', u'-\N{ZERO WIDTH NO-BREAK SPACE}')
 
        pre = post = u''
        if currency.position == 'before':
            pre = u'{symbol}\N{NO-BREAK SPACE}'.format(symbol=currency.symbol or '')
        else:
            post = u'\N{NO-BREAK SPACE}{symbol}'.format(symbol=currency.symbol or '')
 
        return u'{pre}{0}{post}'.format(formatted_amount, pre=pre, post=post)
 
    def _phone_get_country(self, partner):
        if 'country_id' in partner:
            return partner.country_id
        return self.env.user.company_id.country_id
 
    def _msg_sanitization(self, partner, field_name):
        number = partner[field_name]
        if number and _sms_phonenumbers_lib_imported:
            country = self._phone_get_country(partner)
            country_code = country.code if country else None
            try:
                phone_nbr = phonenumbers.parse(number, region=country_code, keep_raw_input=True)
            except phonenumbers.phonenumberutil.NumberParseException:
                return number
            if not phonenumbers.is_possible_number(phone_nbr) or not phonenumbers.is_valid_number(phone_nbr):
                return number
            phone_fmt = phonenumbers.PhoneNumberFormat.E164
            return phonenumbers.format_number(phone_nbr, phone_fmt)
        else:
            return number
             
    def _get_records(self, model):
        if self.env.context.get('active_domain'):
            records = model.search(self.env.context.get('active_domain'))
        elif self.env.context.get('active_ids'):
            records = model.browse(self.env.context.get('active_ids', []))
        else:
            records = model.browse(self.env.context.get('active_id', []))
        return records    


    # @api.model
    # def default_get(self, fields):
    #     result = super(WhatsappComposeMessage, self).default_get(fields)
    #     context = dict(self._context or {})
    #     Attachment = self.env['ir.attachment']
    #     active_model = context.get('active_model')
    #     active_ids = context.get('active_ids')
    #     active_id = context.get('active_id')
    #     msg = result.get('message', '')
    #     result['message'] = msg
    #     #=======================================================================
    #     # UPDATE PATCH
    #     #=======================================================================
    #     WhatsappServer = self.env['ir.whatsapp_server']
    #     whatsapp_id = WhatsappServer.search([('status','=','authenticated')], order='sequence asc', limit=1)
    #     if active_ids and whatsapp_id and ast.literal_eval(str(whatsapp_id.message_response)) and len(active_ids) > ast.literal_eval(str(whatsapp_id.message_response))['block_limit']:
    #         raise UserError(_('Maximum blast message whatsapp is %s.') % str(ast.literal_eval(str(whatsapp_id.message_response))['block_limit']))
    #     #=======================================================================
    #     #result['model'] = active_model
    #     #print ('--active_model--',rec)
    #     partners = self.env['res.partner']
    #     if active_model and active_ids and active_model == 'res.partner':
    #         partners = self.env[active_model].browse(active_ids)
    #         result['model'] = active_model or 'res.partner'
    #         result['partner_ids'] = [(6, 0, partners.ids)]
    #     if active_model and active_ids and active_model != 'res.partner':
    #         active = self.env[active_model].browse(active_id)
    #         if active_model == 'sale.order.line':                
    #             if active.order_partner_id:
    #                 partners = active.order_partner_id
    #                 if active.order_partner_id.child_ids:
    #                     for partner in active.order_partner_id.child_ids:
    #                         partners += partner.id
    #         else:
    #             if active.partner_id:
    #                 partners = active.partner_id
    #                 if active.partner_id.child_ids:
    #                     for partner in active.partner_id.child_ids:
    #                         partners += partner
    #         if not partners:
    #             partners = self.env.user.partner_id
    #         records = self.env[active_model].browse(active_ids)
    #         is_exists = self.env['ir.attachment']
    #         for record in records:
    #             res_name = record.name.replace('/', '_') if active_model == 'account.move' else record.name.replace('/', '_')
    #             domain = [('res_id', '=', record.id), ('name', 'like', res_name + '%'), ('res_model', '=', active_model)] 
    #             is_attachment_exists = Attachment.search(domain, limit=1) if len(active_ids) == 1 else is_exists
    #             #print ('==sss==',is_attachment_exists)
    #             if active_model != 'sale.order.line' and not is_attachment_exists:
    #                 attachments = []
    #                 template = False
    #                 if context.get('template'):
    #                     template = context.get('template')
    #                 elif active_model == 'sale.order':
    #                     template = self.env.ref('sale.email_template_edi_sale')
    #                 elif active_model == 'account.move':
    #                     template = self.env.ref('account.email_template_edi_invoice')
    #                 elif active_model == 'purchase.order':
    #                     if self.env.context.get('send_rfq', False):
    #                         template = self.env.ref('purchase.email_template_edi_purchase')
    #                     else:
    #                         template = self.env.ref('purchase.email_template_edi_purchase_done')
    #                 elif active_model == 'stock.picking':
    #                     template = self.env.ref('stock.mail_template_data_delivery_confirmation')
    #                 elif active_model == 'account.payment':
    #                     template = self.env.ref('account.mail_template_data_payment_receipt')
    #                 if not template:
    #                     break
    #                 #print ('===',report)
    #                 report = template.sudo().report_template
    #                 report_service = report.report_name
    
    #                 if report.report_type not in ['qweb-html', 'qweb-pdf']:
    #                     raise UserError(_('Unsupported report type %s found.') % report.report_type)
    #                 res, format = report._render_qweb_pdf(report, [record.id])
    #                 #pdf = self.env['ir.actions.report'].sudo()._render_qweb_pdf('sale.action_report_saleorder', [order_sudo.id])[0]
    #                 res = base64.b64encode(res)
    #                 if not res_name:
    #                     res_name = 'report.' + report_service
    #                 ext = "." + format
    #                 if not res_name.endswith(ext):
    #                     res_name += ext
    #                 attachments.append((res_name, res))
    #                 #print ('==wwww==',attachments)
    #                 #attachment_ids = []
    #                 for attachment in attachments:
    #                     attachment_data = {
    #                         'name': attachment[0],
    #                         'store_fname': attachment[0],
    #                         'datas': attachment[1],
    #                         'type': 'binary',
    #                         'res_model': active_model,
    #                         'res_id': active_id,
    #                     }
    #                     is_exists += Attachment.create(attachment_data)
    #                 #res, format = report._render_qweb_pdf([record.id])
    #                 # if active_model == 'account.move':
    #                 #     report = self.env['ir.actions.report'].sudo()._render_qweb_pdf("account.account_invoices", record.sudo().id)
    #                 #     filename = res_name + '.' + report[1]
    #                 #     attachment_data = {
    #                 #         'name': filename,#attachment[0],
    #                 #         'store_fname': filename,#attachment[0],
    #                 #         'datas': base64.b64encode(report[0]),#attachment[1],
    #                 #         'type': 'binary',
    #                 #         'res_model': active_model,
    #                 #         'res_id': active_id,
    #                 #         'mimetype': 'application/x-pdf',
    #                 #     }
    #                 #     is_exists = Attachment.create(attachment_data)
    #             else:
    #                 is_exists += is_attachment_exists
    #         result['model'] = active_model or 'res.partner'
    #         result['attachment_ids'] = [(6, 0, is_exists.ids)] if is_exists else []
    #         result['partner_ids'] = [(6, 0, partners.ids)] if partners else []
    #     return result
    
    def _prepare_mail_message(self, author_id, chat_id, record, model, body, data, subject, partner_ids, attachment_ids, response, status):
        #MailMessage = self.env['mail.message']
        #for active_id in active_ids:
        values = {
            'author_id': author_id,
            'model': model or 'res.partner',
            'res_id': record,#model and self.ids[0] or False,
            'body': body,
            'whatsapp_data': data,
            'subject': subject or False,
            'message_type': 'whatsapp',
            'record_name': subject,
            'partner_ids': [(4, pid) for pid in partner_ids],
            'attachment_ids': attachment_ids and [(6, 0, attachment_ids.ids)],
            #'parent_id': parent_id,
            #'subtype_id': subtype_id,
            #'channel_ids': kwargs.get('channel_ids', []),
            #'add_sign': True,
            'whatsapp_method': data['method'],
            'whatsapp_chat_id': chat_id,
            'whatsapp_response': response,
            'whatsapp_status': status,
        }
        # print ('---_prepare_mail_message---',values)
            #MailMessage += MailMessage.sudo().create(values)
        return values#MailMessage.sudo().create(values)

    def whatsapp_message_post_new(self, KlikApi):
        try:
            new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
            uid, context = self.env.uid, self.env.context
            opt_out_list = context.get('mass_whatsapp_opt_out_list') or {}
            message = False
            #with api.Environment.manage():
            #self.env = api.Environment(new_cr, uid, context)
            MailMessage = self.env['mail.message']
            Partners = self.env['res.partner']
            Countries = self.env['res.country']
            for rec in self:
                active_model = rec.model                    
                active_ids = context.get('active_ids') or context.get('active_id') or rec.partner_ids.ids
                print ('---rec---',context,rec)
                if rec.whatsapp_type == 'post':
                    #SEND MESSAGE
                    #MULTI ATTACHMENT
                    message = rec.message
                    partner_ids = context.get('default_partner_ids')
                    #print ('--message--',message)
                    attachment_new_ids = []
                    if rec.sudo().attachment_ids:
                        for attach in rec.sudo().attachment_ids:
                            vals = {'filename': attach.sudo().name}
                            mimetype = guess_mimetype(base64.b64decode(attach.datas))
                            if mimetype == 'application/octet-stream':
                                mimetype = 'video/mp4'
                            str_mimetype = 'data:' + mimetype + ';base64,'
                            attachment = str_mimetype + str(attach.datas.decode("utf-8"))
                            vals.update({'datas': attachment})
                            attachment_new_ids.append(vals)
                    #print ('===DETECT OBJECT===',rec.attachment_ids)
                    for record in self.env[active_model].browse(active_ids):
                        print ('==FOR PARTNER ONLY==',record,active_model)      
                        origin = link = ''
                        amount_total = 0
                        currency_id = False
                        if active_model != 'res.partner':
                            if active_model == 'crm.lead':
                                link = ''#record.get_portal_url()
                                origin = record.name
                                currency_id = record.company_currency
                                amount_total = 0#record.amount_total                                    
                                partner = record.partner_id or record
                            elif active_model == 'sale.order':
                                link = record.get_portal_url()
                                origin = record.name
                                currency_id = record.pricelist_id.currency_id
                                amount_total = record.amount_total                                    
                                partner = record.partner_id
                            elif active_model == 'purchase.order':
                                link = record.get_portal_url()
                                origin = record.name
                                currency_id = record.currency_id
                                amount_total = record.amount_total                                    
                                partner = record.partner_id
                            elif active_model == 'stock.picking':
                                link = ''
                                origin = record.name
                                currency_id = False
                                amount_total = 0
                                partner = record.partner_id
                            elif active_model == 'pos.order':
                                origin = record.name
                                currency_id = record.currency_id
                                amount_total = record.amount_total
                                partner = record.partner_id
                            elif active_model == 'account.move':
                                link = record.get_portal_url()
                                origin = record.name
                                currency_id = record.currency_id
                                amount_total = record.amount_total
                                partner = record.partner_id
                            #print ('#===partners===',partner_ids)
                            if partner_ids:
                                partners = self.env['res.partner'].browse(partner_ids)
                            else:
                                partners = record.partner_id
                        else:
                            partners = record
                        # print ('===PARTNER==',partner)
                        #if partner.whatsapp:
                        if partners:
                            for partner in partners:
                                whatsapp = partner._formatting_mobile_number()
                                print ('=whatsapp=',whatsapp,partner.whatsapp and partner.whatsapp != '0' and whatsapp not in opt_out_list)
                                if partner.whatsapp and partner.whatsapp != '0' and whatsapp not in opt_out_list:                          
                                    whatsapp = partner._formatting_mobile_number()
                                    message_data = {
                                        'method': 'sendMessage',
                                        'phone': whatsapp,
                                        'chatId': partner.chat_id or '',
                                        'body': message.replace('_PARTNER_', partner.name).replace('_NUMBER_', origin).replace('_AMOUNT_TOTAL_', str(self.format_amount(amount_total, currency_id)) if currency_id else '').replace('\xa0', ' ').replace('"', "*").replace("'", "*"),
                                        'origin': origin,
                                        'link': link,
                                    }
                                    if partner.whatsapp == '0' and partner.chat_id:
                                        message_data.update({'phone': '','chatId': partner.chat_id})
                                    #MESSAGE SENT                            
                                    if not attachment_new_ids and message_data['body']:
                                        send_message = {}
                                        # status = 'pending'
                                        data_message = json.dumps(message_data)
                                        #_logger.warning('Failed to send Message to WhatsApp number %s, No body found', whatsapp)
                                        send_message = KlikApi.post_request(method='sendMessage', data=data_message)
                                        if send_message.get('message')['sent']:
                                            status = 'send'
                                            _logger.warning('Success to send Message to WhatsApp number %s', whatsapp)
                                        else:
                                            status = 'error'
                                            _logger.warning('Failed to send Message to WhatsApp number %s', whatsapp)
                                        chatID = partner.chat_id if partner.chat_id else whatsapp#send_message.get('chatID')
                                        # print ('valss1==',chatID)
                                        vals = self._prepare_mail_message(self.env.user.partner_id.id, chatID, record and record.id, active_model, texttohtml.formatHtml(message.replace('_PARTNER_', partner.name).replace('_NUMBER_', origin).replace('_AMOUNT_TOTAL_', str(self.format_amount(amount_total, currency_id)) if currency_id else '').replace('\xa0', ' ')), message_data, rec.subject, [partner.id], [], send_message, status)
                                        # print ('valss2==',vals)
                                        MailMessage += MailMessage.sudo().create(vals)
                                        #partner.chat_id = chatID
                                        new_cr.commit()
                                    #ATTACHMENT SENT
                                    elif attachment_new_ids:
                                        for att in attachment_new_ids:
                                            # print ('==Whatsapp Server=',att)
                                            message_attach = {
                                                'method': 'sendFile',
                                                'phone': whatsapp,
                                                'chatId': partner.chat_id or '',
                                                'body': att['datas'].split(",")[0],
                                                'filename': att['filename'],
                                                'caption': message.replace('_PARTNER_', partner.name).replace('_NUMBER_', origin).replace('_AMOUNT_TOTAL_', str(self.format_amount(amount_total, currency_id)) if currency_id else '').replace('\xa0', ' '),#att['caption'],
                                                'origin': origin,
                                                'link': link,
                                            }
                                            #SENT ATTAHCMENT
                                            if message_attach['body']:
                                                send_attach = {}
                                                status = 'pending'
                                        chatID = partner.chat_id if partner.chat_id else whatsapp#send_attach.get('chatID')
                                        vals = self._prepare_mail_message(self.env.user.partner_id.id, chatID, record and record.id, active_model, texttohtml.formatHtml(message.replace('_PARTNER_', partner.name).replace('_NUMBER_', origin).replace('_AMOUNT_TOTAL_', str(self.format_amount(amount_total, currency_id)) if currency_id else '').replace('\xa0', ' ')), message_attach, rec.subject, [partner.id], rec.attachment_ids, send_attach, status)
                                        MailMessage += MailMessage.sudo().create(vals)
                                        #partner.chat_id = chatID
                                        new_cr.commit()
                        # else:
                        #     whatsapp = partner._formatting_mobile_number()
                        #     if partner.whatsapp and partner.whatsapp != '0' and whatsapp not in opt_out_list:                          
                        #         whatsapp = partner._formatting_mobile_number()
                        #         message_data = {
                        #             'method': 'sendMessage',
                        #             'phone': whatsapp,
                        #             'chatId': partner.chat_id or '',
                        #             'body': message.replace('_PARTNER_', partner.name).replace('_NUMBER_', origin).replace('_AMOUNT_TOTAL_', str(self.format_amount(amount_total, currency_id)) if currency_id else '').replace('\xa0', ' ').replace('"', "*").replace("'", "*"),
                        #             'origin': origin,
                        #             'link': link,
                        #         }
                        #         if partner.whatsapp == '0' and partner.chat_id:
                        #             message_data.update({'phone': '','chatId': partner.chat_id})
                        #         #MESSAGE SENT                            
                        #         if not attachment_new_ids and message_data['body']:
                        #             send_message = {}
                        #             status = 'pending'
                        #             # data_message = json.dumps(message_data)
                        #             # #_logger.warning('Failed to send Message to WhatsApp number %s, No body found', whatsapp)
                        #             # send_message = KlikApi.post_request(method='sendMessage', data=data_message)
                        #             # if send_message.get('message')['sent']:
                        #             #     status = 'send'
                        #             #     _logger.warning('Success to send Message to WhatsApp number %s', whatsapp)
                        #             # else:
                        #             #     status = 'error'
                        #             #     _logger.warning('Failed to send Message to WhatsApp number %s', whatsapp)
                        #             chatID = partner.chat_id if partner.chat_id else whatsapp#send_message.get('chatID')
                        #             vals = self._prepare_mail_message(self.env.user.partner_id.id, chatID, record and record.id, active_model, texttohtml.formatHtml(message.replace('_PARTNER_', partner.name).replace('_NUMBER_', origin).replace('_AMOUNT_TOTAL_', str(self.format_amount(amount_total, currency_id)) if currency_id else '').replace('\xa0', ' ')), message_data, rec.subject, [partner.id], [], send_message, status)
                        #             MailMessage.sudo().create(vals)
                        #             #partner.chat_id = chatID
                        #             new_cr.commit()
                        #         #ATTACHMENT SENT
                        #         elif attachment_new_ids:
                        #             for att in attachment_new_ids:
                        #                 message_attach = {
                        #                     'method': 'sendFile',
                        #                     'phone': whatsapp,
                        #                     'chatId': partner.chat_id or '',
                        #                     'body': att['datas'].split(",")[0],
                        #                     'filename': att['filename'],
                        #                     'caption': message.replace('_PARTNER_', partner.name).replace('_NUMBER_', origin).replace('_AMOUNT_TOTAL_', str(self.format_amount(amount_total, currency_id)) if currency_id else '').replace('\xa0', ' '),#att['caption'],
                        #                     'origin': origin,
                        #                     'link': link,
                        #                 }
                        #                 #SENT ATTAHCMENT
                        #                 if message_attach['body']:
                        #                     send_attach = {}
                        #                     status = 'pending'
                        #                     # data_attach = json.dumps(message_attach)
                        #                     # #_logger.warning('Failed to send Message to WhatsApp number %s, No attachment found', whatsapp)
                        #                     # send_attach = KlikApi.post_request(method='sendFile', data=data_attach)
                        #                     # if send_attach.get('message')['sent']:        
                        #                     #     status = 'send'                
                        #                     #     _logger.warning('Success to send Attachment to WhatsApp number %s', whatsapp)
                        #                     # else:
                        #                     #     status = 'error'
                        #                     #     _logger.warning('Failed to send Attachment to WhatsApp number %s', whatsapp)
                        #                     chatID = partner.chat_id if partner.chat_id else whatsapp#send_attach.get('chatID')
                        #                     vals = self._prepare_mail_message(self.env.user.partner_id.id, chatID, record and record.id, active_model, texttohtml.formatHtml(message.replace('_PARTNER_', partner.name).replace('_NUMBER_', origin).replace('_AMOUNT_TOTAL_', str(self.format_amount(amount_total, currency_id)) if currency_id else '').replace('\xa0', ' ')), message_attach, rec.subject, [partner.id], rec.attachment_ids, send_attach, status)
                        #                     MailMessage.sudo().create(vals)
                        #                     #partner.chat_id = chatID
                        #                     new_cr.commit()
                            #time.sleep(3)
                elif rec.whatsapp_type == 'get' and rec.type in ('contact', 'group'):
                    #CREATE GROUP OR CONTACT
                    dialogs = {}
                    #data_dialog = json.dumps(dialogs)
                    get_dialog = KlikApi.get_request(method='dialogs', data=dialogs)
                    #print ('-get_dialog--',get_dialog)
                    if get_dialog.get('dialogs'):
                        for dialog in get_dialog.get('dialogs'):
                            #print ('---dialog---',dialog)
                            if rec.type == 'contact' and dialog.get('id') and '@c.us' in dialog.get('id'):
                                ContactsExist = Partners.sudo().search([('chat_id','=',dialog.get('id'))], limit=1)
                                whatsapp = dialog.get('id').replace('@c.us','')
                                country = Countries.search([('phone_code','=',whatsapp[:2])], limit=1)
                                whatsapp_number = '0'+whatsapp[2:]
                                if not ContactsExist:                                        
                                    vals = {
                                        'name': dialog.get('subject') if 'subject' in dialog else dialog.get('name'),
                                        'whatsapp': whatsapp_number,
                                        'chat_id': dialog.get('id'),
                                        'whatsapp_type': '@c.us',
                                        #'customer': True,
                                        'country_id':country.id,
                                    }
                                    Partners.create(vals)
                                    _logger.warning('Added Whatsapp Contact %s**** to Partner Odoo', whatsapp_number[:5])                                                                 
                                    new_cr.commit()
                                    #time.sleep(3)
                                else:
                                    for part in ContactsExist:
                                        part.write({'name': dialog.get('subject') if 'subject' in dialog else dialog.get('name')})       
                                        _logger.warning('Updated Whatsapp Contact %s**** to Partner Odoo', whatsapp_number[:5])                                     
                                        new_cr.commit()
                                        #time.sleep(3)
                            elif rec.type == 'group' and dialog.get('id') and '@g.us'  in dialog.get('id'): 
                                GroupsExist = Partners.sudo().search([('chat_id','=',dialog.get('id'))], limit=1)
                                whatsapp = dialog.get('id')
                                country = Countries.search([('phone_code','=',whatsapp[:2])], limit=1)
                                if not GroupsExist:                              
                                    vals = {
                                        'name': dialog.get('subject') if 'subject' in dialog else dialog.get('name'),
                                        'whatsapp': dialog.get('id').replace('@g.us',''),
                                        'chat_id': dialog.get('id'),
                                        'whatsapp_type': '@g.us',
                                        'country_id':country.id,
                                    }
                                    Partners.create(vals)
                                    _logger.warning('Added Whatsapp Group *%s* to Partner Odoo', dialog.get('subject') if 'subject' in dialog else dialog.get('name'))    
                                    new_cr.commit()
                                    #time.sleep(3)
                                else:
                                    for part in GroupsExist:
                                        part.write({'name': dialog.get('subject') if 'subject' in dialog else dialog.get('name')})
                                        _logger.warning('Update Whatsapp Group *%s* to Partner Odoo', dialog.get('subject') if 'subject' in dialog else dialog.get('name'))    
                                        new_cr.commit()
                                        #time.sleep(3)
                #return MailMessage
        finally:
            pass
            #self.env.cr.close()


    def whatsapp_message_post(self):
        # print ("""==Send whatsapp message via threding==.""")
        KlikApi = False
        # messages = self.env['mail.message']
        WhatsappServer = self.env['ir.whatsapp_server']
        domain = WhatsappServer._find_default_for_server()
        whatsapp_ids = WhatsappServer.search(domain, order='sequence asc', limit=1)
        # print ('===_find_default_for_server===',whatsapp_ids)
        #for wserver in whatsapp_ids.filtered(lambda ws: ast.literal_eval(str(ws.message_response))['limit_qty'] >= int(ws.message_counts)):
        
        # for wserver in whatsapp_ids.filtered(lambda ws: not ast.literal_eval(str(ws.message_response))['block']):
        #     KlikApi = wserver.klikapi()
        #     KlikApi.auth()
        #     thread_start = threading.Thread(target=self.whatsapp_message_post_new(KlikApi))
        #     thread_start.start()
        try:
            for wserver in whatsapp_ids.filtered(lambda ws: not ast.literal_eval(str(ws.message_response))['block']):
                # if wserver.status != 'authenticated':
                #     _logger.warning('Whatsapp Authentication Failed!\nConfigure Whatsapp Configuration in General Setting.')
                KlikApi = wserver.klikapi()
                KlikApi.auth()
                thread_start = threading.Thread(target=self.whatsapp_message_post_new(KlikApi))
                thread_start.start()
                #self.env['mail.message']._resend_whatsapp_message_resend(KlikApi)
                #break
        except:
            _logger.warning('Whatsapp Authentication Failed!\nConfigure Whatsapp Configuration in General Setting.')
        # return True
        #print ('--KlikApi--',messages)
        #return messages._resend_whatsapp_message_resend(KlikApi)
