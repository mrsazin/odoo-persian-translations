/** @odoo-module */


import { renderToElement } from "@web/core/utils/render";
import { SaleDetailsButton } from "@point_of_sale/app/navbar/sale_details_button/sale_details_button";
import { patch } from "@web/core/utils/patch";

patch(SaleDetailsButton.prototype,{
    async onClick() {
        // IMPROVEMENT: Perhaps put this logic in a parent component
        // so that for unit testing, we can check if this simple
        // component correctly triggers an event.
        const saleDetails = await this.orm.call(
            "report.point_of_sale.report_saledetails",
            "get_sale_details",
            [false, false, false, [this.pos.pos_session.id]]
        );
        const report = renderToElement(
            "point_of_sale.SaleDetailsReport",
            Object.assign({}, saleDetails, {
                date: moment().format('jYYYY-jMM-jDD HH:mm:ss'),
                pos: this.pos,
                formatCurrency: this.env.utils.formatCurrency,
            })
        );
        const { successful, message } = await this.hardwareProxy.printer.printReceipt(report);
        if (!successful) {
            await this.popup.add(ErrorPopup, {
                title: message.title,
                body: message.body,
            });
        }
    }
});

