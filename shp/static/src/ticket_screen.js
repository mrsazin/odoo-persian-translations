/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { deserializeDateTime, formatDateTime } from "@shp/lib/shpdates";
import { _t } from "@web/core/l10n/translation";

const { DateTime } = luxon;

import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { patch } from "@web/core/utils/patch";

patch(TicketScreen.prototype, {
    getDate(order) {
        return formatDateTime(order.date_order);
    },
    _getSearchFields() {
        const fields = {
            TRACKING_NUMBER: {
                repr: (order) => order.trackingNumber,
                displayName: _t("Order Number"),
                modelField: "tracking_number",
            },
            RECEIPT_NUMBER: {
                repr: (order) => order.name,
                displayName: _t("Receipt Number"),
                modelField: "pos_reference",
            },
            DATE: {
                repr: (order) => formatDateTime(order.date_order),
                displayName: _t("Date"),
                modelField: "date_order",
            },
            PARTNER: {
                repr: (order) => order.get_partner_name(),
                displayName: _t("Customer"),
                modelField: "partner_id.complete_name",
            },
        };

        if (this.showCardholderName()) {
            fields.CARDHOLDER_NAME = {
                repr: (order) => order.get_cardholder_name(),
                displayName: _t("Cardholder Name"),
                modelField: "payment_ids.cardholder_name",
            };
        }

        return fields;
    },
    async _fetchSyncedOrders() {
        const domain = this._computeSyncedOrdersDomain();
        const limit = this._state.syncedOrders.nPerPage;
        const offset =
            (this._state.syncedOrders.currentPage - 1) * this._state.syncedOrders.nPerPage;
        const config_id = this.pos.config.id;
        const { ordersInfo, totalCount } = await this.orm.call(
            "pos.order",
            "search_paid_order_ids",
            [],
            { config_id, domain, limit, offset }
        );
        const idsNotInCache = ordersInfo.filter(
            (orderInfo) => !(orderInfo[0] in this._state.syncedOrders.cache)
        );
        // If no cacheDate, then assume reasonable earlier date.
        const cacheDate = this._state.syncedOrders.cacheDate || DateTime.fromMillis(0);
        const idsNotUpToDate = ordersInfo.filter((orderInfo) => {
            return deserializeDateTime(orderInfo[1]) > cacheDate;
        });
        const idsToLoad = idsNotInCache.concat(idsNotUpToDate).map((info) => info[0]);
        if (idsToLoad.length > 0) {
            const fetchedOrders = await this.orm.call("pos.order", "export_for_ui", [idsToLoad]);
            // Check for missing products and partners and load them in the PoS
            await this.pos._loadMissingProducts(fetchedOrders);
            await this.pos._loadMissingPartners(fetchedOrders);
            // Cache these fetched orders so that next time, no need to fetch
            // them again, unless invalidated. See `_onInvoiceOrder`.
            fetchedOrders.forEach((order) => {
                this._state.syncedOrders.cache[order.id] = new Order(
                    { env: this.env },
                    { pos: this.pos, json: order }
                );
            });
            //Update the datetime indicator of the cache refresh
            this._state.syncedOrders.cacheDate = DateTime.local();
        }

        const ids = ordersInfo.map((info) => info[0]);
        this._state.syncedOrders.totalCount = totalCount;
        this._state.syncedOrders.toShow = ids.map((id) => this._state.syncedOrders.cache[id]);
    }
});
