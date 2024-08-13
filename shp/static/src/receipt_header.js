/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
   getReceiptHeaderData() {
       return {
           ...super.getReceiptHeaderData(...arguments),
           order_name: this.get_order().name,
           order_date: moment(this.get_order().receiptDate, 'jYYYY-jMM-jDD HH:mm:ss').format('jYYYY/jMM/jDD HH:mm:ss'),
       };
   },
});