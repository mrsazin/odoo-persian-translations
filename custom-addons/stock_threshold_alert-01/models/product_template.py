from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_min_stock_threshold = fields.Float(
        string="Minimum Stock Threshold",
        help="Minimum quantity to trigger low stock notification"
    )
