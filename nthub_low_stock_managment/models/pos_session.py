# -*- coding: utf-8 -*-
from odoo import models


class PosSession(models.Model):
    """Inherited pos session for loading quantity fields from product"""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Load forcast and on hand quantity field to pos session.
           :return dict: returns dictionary of field parameters for the
                        product model
        """
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('qty_available')
        result['search_params']['fields'].append('min_low_stock_alert')
        return result
