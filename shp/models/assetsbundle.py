# -*- coding: utf-8 -*-

import logging
import os


from odoo.addons.base.models.assetsbundle import WebAsset

_logger = logging.getLogger(__name__)

ANY_UNIQUE = '_' * 7
EXTENSIONS = (".js", ".css", ".scss", ".sass", ".less", ".xml")


class sWebAsset(object):
    _inherit = 'odoo.addons.base.models.assetsbundle.WebAsset'
    
    @property
    def last_modified(self):
        if self._last_modified is None:
            try:
                self.stat()
            except Exception:  # most likely nor a file or an attachment, skip it
                pass
            if self._filename and self.bundle.is_debug_assets:  # usually _last_modified should be set exept in debug=assets
                self._last_modified = os.path.getmtime(self._filename)
            elif self._ir_attach:
                self._last_modified = self._ir_attach.write_date
            if not self._last_modified:
                self._last_modified = -1
        return self._last_modified

WebAsset.last_modified = sWebAsset.last_modified