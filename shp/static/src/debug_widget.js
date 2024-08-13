/** @odoo-module **/

import { DebugWidget } from "@point_of_sale/app/debug/debug_widget";
import { patch } from "@web/core/utils/patch";

import { _t } from "@web/core/l10n/translation";
import { serializeDateTime } from "@shp/lib/shpdates";

patch(DebugWidget.prototype, {
    get paidOrdersFilename() {
        return `${_t("paid orders")} ${serializeDateTime(moment().format('jYYYY-jMM-jDD HH:mm:ss')).replace(
            /:|\s/gi,
            "-"
        )}.json`;
    },
    get unpaidOrdersFilename() {
        return `${_t("unpaid orders")} ${serializeDateTime(moment().format('jYYYY-jMM-jDD HH:mm:ss')).replace(
            /:|\s/gi,
            "-"
        )}.json`;
    }
});
