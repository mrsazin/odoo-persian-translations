/** @odoo-module */

import { ErrorTracebackPopup } from "@point_of_sale/app/errors/popups/error_traceback_popup";
import { patch } from "@web/core/utils/patch";

import { _t } from "@web/core/l10n/translation";
import { serializeDateTime } from "@shp/lib/shpdates";





const { DateTime } = luxon;

// formerly ErrorTracebackPopupWidget
patch(ErrorTracebackPopup.prototype, {
    get tracebackFilename() {
        return `${_t("error")} ${serializeDateTime(moment().format('jYYYY-jMM-jDD HH:mm:ss')).replace(/:|\s/gi, "-")}.txt`;
    }
});