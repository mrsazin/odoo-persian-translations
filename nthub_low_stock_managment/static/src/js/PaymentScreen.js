/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async _finalizeValidation() {
        await super._finalizeValidation()
        if (this.currentOrder && this.currentOrder.orderlines)
        {
            for (let line of this.currentOrder.orderlines)
            {
                line.product.qty_available = line.product.qty_available - line.quantity
            }
        }
    },
});
