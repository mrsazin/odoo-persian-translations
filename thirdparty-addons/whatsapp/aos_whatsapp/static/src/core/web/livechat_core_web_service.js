/* @odoo-module */

import { reactive } from "@odoo/owl";

import { registry } from "@web/core/registry";

export class WhatsappCoreWeb {
    constructor(env, services) {
        Object.assign(this, {
            busService: services.bus_service,
        });
        /** @type {import("@mail/core/common/messaging_service").Messaging} */
        this.messagingService = services["mail.messaging"];
        /** @type {import("@mail/core/common/store_service").Store} */
        this.store = services["mail.store"];
    }

    setup() {
        this.messagingService.isReady.then((data) => {
            if (data.current_user_settings?.is_discuss_sidebar_category_whatsapp_open) {
                this.store.discuss.whatsapp.isOpen = true;
            }
            this.busService.subscribe("res.users.settings", (payload) => {
                if (payload) {
                    this.store.discuss.whatsapp.isOpen =
                        payload.is_discuss_sidebar_category_whatsapp_open ??
                        this.store.discuss.whatsapp.isOpen;
                }
            });
        });
    }
}

export const whatsappCoreWeb = {
    dependencies: ["bus_service", "mail.messaging", "mail.store"],
    start(env, services) {
        const whatsappCoreWeb = reactive(new WhatsappCoreWeb(env, services));
        whatsappCoreWeb.setup();
        return whatsappCoreWeb;
    },
};

registry.category("services").add("im_whatsapp.core.web", whatsappCoreWeb);
