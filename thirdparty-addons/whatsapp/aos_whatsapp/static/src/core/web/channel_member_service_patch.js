/* @odoo-module */

import { ChannelMemberService } from "@mail/core/common/channel_member_service";
import { patch } from "@web/core/utils/patch";

patch(ChannelMemberService.prototype, {
    getName(member) {
        if (member.thread.type !== "whatsapp") {
            return super.getName(member);
        }
        if (member.persona.user_whatsapp_username) {
            return member.persona.user_whatsapp_username;
        }
        if (member.persona.is_public) {
            return member.thread.anonymous_name;
        }
        return super.getName(member);
    },
});
