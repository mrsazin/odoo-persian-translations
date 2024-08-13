/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";


// function getDateFormat(uDate,option){
//     let date = new Intl.DateTimeFormat('fa-IR', option).format(uDate);
//     return date;
// } 
patch(Order.prototype, {
   export_for_printing() {
       const result = super.export_for_printing(...arguments);
    //    var loyalty_points = Math.floor(Math.round(result.amount_total * 2))
    //    result.loyalty_points = loyalty_points
    
    var order_date = new Date(result.date);
    result.date = new Date(order_date).toLocaleString('fa-IR');
    
    return result;
   },
});

