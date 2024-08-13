# # -*- coding: utf-8 -*-

# import khayyam
# import pytz
# from odoo import api, fields, models
# import odoo.addons.shp.common.fields as myfields


# class SaleOrder(models.Model):
#     _inherit = 'sale.order'    

#     @api.depends("validity_date")
#     def _compute_validity_date_jalali(self):
#         for record in self:
#             # from_zone = pytz.utc
#             # to_zone = pytz.timezone('Asia/Tehran')
#             # local_timestamp = record.validity_date.replace(tzinfo=from_zone).astimezone(to_zone)
#             # record.validity_date = khayyam.JalaliDatetime(local_timestamp, khayyam.TehranTimezone)
#             record.validity_date = myfields.Datetime.to_datetime(local_timestamp, khayyam.TehranTimezone)

#     validity_date = fields.Char(
#         string="Expiration Date SHP",
#         compute='_compute_validity_date_jalali',
#         store=True, readonly=False, copy=False, precompute=True)

#     @api.depends("commitment_date")
#     def _compute_commitment_date_jalali(self):
#         for record in self:
#             from_zone = pytz.utc
#             to_zone = pytz.timezone('Asia/Tehran')
#             local_timestamp = record.commitment_date.replace(tzinfo=from_zone).astimezone(to_zone)
#             record.commitment_date = khayyam.JalaliDatetime(local_timestamp, khayyam.TehranTimezone)

#     commitment_date = fields.Char(
#         string="Commitment Date SHP",
#         compute='_compute_commitment_date_jalali',
#         store=True, readonly=False, copy=False, precompute=True)
    
#     def func_shamsi(arg):
#         return 'testttttt'
