/* @odoo-module */

import { Composer } from "@mail/core/common/composer";

import { patch } from "@web/core/utils/patch";

patch(Composer.prototype, {
    onKeydown(ev) {
        super.onKeydown(ev);
        if (
            ev.key === "Tab" &&
            this.thread?.type === "whatsapp" &&
            !this.props.composer.textInputContent
        ) {
            const threadChanged = this.threadService.goToOldestUnreadWhatsappThread();
            if (threadChanged) {
                // prevent chat window from switching to the next thread: as
                // we want to go to the oldest unread thread, not the next
                // one.
                ev.stopPropagation();
            }
        }
    },

    displayNextWhatsappHint() {
        return (
            this.thread?.type === "whatsapp" &&
            !this.env.inChatWindow &&
            this.store.discuss.whatsapp.threads.some(
                (thread) => thread.notEq(this.thread) && thread.isUnread
            )
        );
    },
});
