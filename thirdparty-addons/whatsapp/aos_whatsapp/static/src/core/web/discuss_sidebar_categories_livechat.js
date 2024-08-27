/* @odoo-module */

import { discussSidebarCategoriesRegistry } from "@mail/discuss/core/web/discuss_sidebar_categories";

discussSidebarCategoriesRegistry.add(
    "whatsapps",
    {
        predicate: (store) =>
            store.discuss.whatsapp.threads.some(
                (thread) => thread.displayToSelf || thread.isLocallyPinned
            ),
        value: (store) => store.discuss.whatsapp,
    },
    { sequence: 20 }
);
