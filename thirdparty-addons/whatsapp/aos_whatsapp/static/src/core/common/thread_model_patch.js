/* @odoo-module */

import { Record } from "@mail/core/common/record";
import { Thread } from "@mail/core/common/thread_model";

import { patch } from "@web/core/utils/patch";

patch(Thread, {
    _insert(data) {
        const thread = super._insert(...arguments);
        if (thread.type === "whatsapp") {
            if (data?.operator_pid) {
                thread.operator = {
                    type: "partner",
                    id: data.operator_pid[0],
                    name: data.operator_pid[1],
                };
            }
        }
        return thread;
    },
});

patch(Thread.prototype, {
    setup() {
        super.setup();
        this.operator = Record.one("Persona");
    },

    get typesAllowingCalls() {
        return super.typesAllowingCalls.concat(["whatsapp"]);
    },

    get isChatChannel() {
        return this.type === "whatsapp" || super.isChatChannel;
    },
});
