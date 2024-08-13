/** @odoo-module */

import { Order, PosCollection, Product, Payment } from "@point_of_sale/app/store/models";
import { constructFullProductName, random5Chars, uuidv4, qrCodeSrc } from "@point_of_sale/utils";
import { _t } from "@web/core/l10n/translation";
import {
    formatDate,
    formatDateTime,
    serializeDateTime,
    deserializeDate,
    deserializeDateTime,
} from "@shp/lib/shpdates";
import { patch } from "@web/core/utils/patch";
import { omit } from "@web/core/utils/objects";

// const SERVER_DATE_FORMAT = "yyyy-MM-dd";
// const SERVER_TIME_FORMAT = "HH:mm:ss";
// const SERVER_DATETIME_FORMAT = `${SERVER_DATE_FORMAT} ${SERVER_TIME_FORMAT}`;
const SERVER_DATETIME_FORMAT_JALALI = 'jYYYY-jMM-jDD HH:mm:ss';
const SERVER_DATETIME_FORMAT_GEORGIAN = 'YYYY-MM-DD HH:mm:ss';
const SERVER_DATE_FORMAT_JALALI = 'jYYYY-jMM-jDD';
const SERVER_DATE_FORMAT_GEORGIAN = 'YYYY-MM-DD';

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
                        
        // let now = moment().format('YYYY-M-D HH:mm:ss');
        // let converted = moment(now).format('jYYYY-jMM-jDD HH:mm:ss');
        // let now_utc = moment(now).utc().format('YYYY-M-D HH:mm:ss');
        // let converted_utc = moment(now_utc).format('jYYYY-jMM-jDD HH:mm:ss');
        
        var self = this;
        options = options || {};

        this.locked = false;
        this.pos = options.pos;
        this.selected_orderline = undefined;
        this.selected_paymentline = undefined;
        this.screen_data = {}; // see Gui
        this.temporary = options.temporary || false;
        this.date_order = moment().format('jYYYY-jMM-jDD HH:mm:ss');
        this.to_invoice = false;
        this.orderlines = new PosCollection();
        this.paymentlines = new PosCollection();
        this.pos_session_id = this.pos.pos_session.id;
        this.cashier = this.pos.get_cashier();
        this.finalized = false; // if true, cannot be modified.
        this.shippingDate = null;
        this.firstDraft = true;
        this.combos = [];

        this.partner = null;

        this.uiState = {
            ReceiptScreen: {
                inputEmail: "",
                // if null: not yet tried to send
                // if false/true: tried sending email
                emailSuccessful: null,
                emailNotice: "",
            },
            // TODO: This should be in pos_restaurant.
            TipScreen: {
                inputTipAmount: "",
            },
        };

        if (options.json) {
            this.init_from_JSON(options.json);
            const linesById = Object.fromEntries(this.orderlines.map((l) => [l.id || l.cid, l]));
            for (const line of this.orderlines) {
                line.comboLines = line.combo_line_ids?.map((id) => linesById[id]);
                const combo_parent_id = line.combo_parent_id?.[0] || line.combo_parent_id;
                if (combo_parent_id) {
                    line.comboParent = linesById[combo_parent_id];
                }
            }
        } else {
            this.set_pricelist(this.pos.default_pricelist);
            this.sequence_number = this.pos.pos_session.sequence_number++;
            this.access_token = uuidv4(); // unique uuid used to identify the authenticity of the request from the QR code.
            this.ticketCode = this._generateTicketCode(); // 5-digits alphanum code shown on the receipt
            this.uid = this.generate_unique_id();
            this.name = _t("Order %s", this.uid);
            this.fiscal_position = this.pos.fiscal_positions.find(function (fp) {
                return fp.id === self.pos.config.default_fiscal_position_id[0];
            });
        }

        this.lastOrderPrepaChange = this.lastOrderPrepaChange || {};
        this.trackingNumber = (
            (this.pos_session_id % 10) * 100 +
            (this.sequence_number % 100)
        ).toString();
    },
    init_from_JSON(json) {
        let partner;
        if (json.state && ["done", "invoiced", "paid"].includes(json.state)) {
            this.sequence_number = json.sequence_number;
            this.pos_session_id = json.pos_session_id;
        } else if (json.pos_session_id !== this.pos.pos_session.id) {
            this.sequence_number = this.pos.pos_session.sequence_number++;
        } else {
            this.sequence_number = json.sequence_number;
            this.pos.pos_session.sequence_number = Math.max(
                this.sequence_number + 1,
                this.pos.pos_session.sequence_number
            );
        }
        this.session_id = this.pos.pos_session.id;
        this.uid = json.uid;
        if (json.name) {
            this.name = json.name;
        } else {
            this.name = _t("Order %s", this.uid);
        }
        this.date_order = deserializeDateTime(json.date_order);
        this.server_id = json.server_id || json.id || false;
        this.user_id = json.user_id;
        this.firstDraft = false;

        if (json.fiscal_position_id) {
            var fiscal_position = this.pos.fiscal_positions.find(function (fp) {
                return fp.id === json.fiscal_position_id;
            });

            if (fiscal_position) {
                this.fiscal_position = fiscal_position;
            } else {
                this.fiscal_position_not_found = true;
                console.error("ERROR: trying to load a fiscal position not available in the pos");
            }
        }

        if (json.pricelist_id) {
            this.pricelist = this.pos.pricelists.find(function (pricelist) {
                return pricelist.id === json.pricelist_id;
            });
        } else {
            this.pricelist = this.pos.default_pricelist;
        }

        if (json.partner_id) {
            partner = this.pos.db.get_partner_by_id(json.partner_id);
            if (!partner) {
                console.error("ERROR: trying to load a partner not available in the pos");
            }
        } else {
            partner = null;
        }
        this.partner = partner;

        this.temporary = false; // FIXME
        this.to_invoice = json.to_invoice || false;
        this.shippingDate = json.shipping_date;

        var orderlines = json.lines;
        for (var i = 0; i < orderlines.length; i++) {
            var orderline = orderlines[i][2];
            if (orderline.product_id && this.pos.db.get_product_by_id(orderline.product_id)) {
                this.add_orderline(
                    new Orderline(
                        { env: this.env },
                        { pos: this.pos, order: this, json: orderline }
                    )
                );
            }
        }

        var paymentlines = json.statement_ids;
        for (i = 0; i < paymentlines.length; i++) {
            var paymentline = paymentlines[i][2];
            var newpaymentline = new Payment(
                { env: this.env },
                { pos: this.pos, order: this, json: paymentline }
            );
            this.paymentlines.add(newpaymentline);

            if (i === paymentlines.length - 1) {
                this.select_paymentline(newpaymentline);
            }
        }

        // Tag this order as 'locked' if it is already paid.
        this.locked = ["paid", "done", "invoiced"].includes(json.state);
        this.state = json.state;
        this.amount_return = json.amount_return;
        this.account_move = json.account_move;
        this.backendId = json.id;
        this.is_tipped = json.is_tipped || false;
        this.tip_amount = json.tip_amount || 0;
        this.access_token = json.access_token || "";
        this.ticketCode = json.ticket_code || "";
        this.lastOrderPrepaChange =
            json.last_order_preparation_change && JSON.parse(json.last_order_preparation_change);
    },
    export_as_JSON() {
        var orderLines, paymentLines;
        orderLines = [];
        this.orderlines.forEach((item) => {
            return orderLines.push([0, 0, item.export_as_JSON()]);
        });
        paymentLines = [];
        this.paymentlines.forEach((item) => {
            const itemAsJson = item.export_as_JSON();
            if (itemAsJson) {
                return paymentLines.push([0, 0, itemAsJson]);
            }
        });
        var json = {
            name: this.get_name(),
            amount_paid: this.get_total_paid() - this.get_change(),
            amount_total: this.get_total_with_tax(),
            amount_tax: this.get_total_tax(),
            amount_return: this.get_change(),
            lines: orderLines,
            statement_ids: paymentLines,
            pos_session_id: this.pos_session_id,
            pricelist_id: this.pricelist ? this.pricelist.id : false,
            partner_id: this.get_partner() ? this.get_partner().id : false,
            user_id: this.pos.user.id,
            uid: this.uid,
            sequence_number: this.sequence_number,
            date_order: serializeDateTime(this.date_order),
            fiscal_position_id: this.fiscal_position ? this.fiscal_position.id : false,
            server_id: this.server_id ? this.server_id : false,
            to_invoice: this.to_invoice ? this.to_invoice : false,
            shipping_date: this.shippingDate ? this.shippingDate : false,
            is_tipped: this.is_tipped || false,
            tip_amount: this.tip_amount || 0,
            access_token: this.access_token || "",
            last_order_preparation_change: JSON.stringify(this.lastOrderPrepaChange),
            ticket_code: this.ticketCode || "",
        };
        if (!this.is_paid && this.user_id) {
            json.user_id = this.user_id;
        }
        return json;
    },
    export_for_printing() {
        // If order is locked (paid), the 'change' is saved as negative payment,
        // and is flagged with is_change = true. A receipt that is printed first
        // time doesn't show this negative payment so we filter it out.
        const paymentlines = this.paymentlines
            .filter((p) => !p.is_change)
            .map((p) => p.export_for_printing());
        this.receiptDate ||= moment().format('jYYYY-jMM-jDD HH:mm:ss');
        return {
            orderlines: this.orderlines.map((l) => omit(l.getDisplayData(), "internalNote")),
            paymentlines,
            amount_total: this.get_total_with_tax(),
            total_without_tax: this.get_total_without_tax(),
            amount_tax: this.get_total_tax(),
            total_paid: this.get_total_paid(),
            total_discount: this.get_total_discount(),
            rounding_applied: this.get_rounding_applied(),
            tax_details: this.get_tax_details(),
            change: this.locked ? this.amount_return : this.get_change(),
            name: this.get_name(),
            invoice_id: null, //TODO
            cashier: this.cashier?.name,
            date: this.receiptDate,
            pos_qr_code:
                this.pos.company.point_of_sale_use_ticket_qr_code &&
                (this.finalized || ["paid", "done", "invoiced"].includes(this.state)) &&
                qrCodeSrc(
                    `${this.pos.base_url}/pos/ticket/validate?access_token=${this.access_token}`
                ),
            ticket_code:
                this.pos.company.point_of_sale_ticket_unique_code &&
                this.finalized &&
                this.ticketCode,
            base_url: this.pos.base_url,
            footer: this.pos.config.receipt_footer,
            // FIXME: isn't there a better way to handle this date?
            shippingDate:
                //this.shippingDate && formatDate( DateTime.fromJSDate(new Date(this.shippingDate))),
                this.shippingDate && moment(this.shippingDate).format('jYYYY-jMM-jDD HH:mm:ss'),
            headerData: {
                ...this.pos.getReceiptHeaderData(this),
                trackingNumber: this.trackingNumber,
            },
        };
    }
});

patch(Product.prototype, {
    get_price(pricelist, quantity, price_extra = 0, recurring = false) {
        const date = moment().format('jYYYY-jMM-jDD HH:mm:ss');

        // In case of nested pricelists, it is necessary that all pricelists are made available in
        // the POS. Display a basic alert to the user in the case where there is a pricelist item
        // but we can't load the base pricelist to get the price when calling this method again.
        // As this method is also call without pricelist available in the POS, we can't just check
        // the absence of pricelist.
        if (recurring && !pricelist) {
            alert(
                _t(
                    "An error occurred when loading product prices. " +
                        "Make sure all pricelists are available in the POS."
                )
            );
        }

        const rules = !pricelist
            ? []
            : (this.applicablePricelistItems[pricelist.id] || []).filter((item) =>
                  this.isPricelistItemUsable(item, date)
              );

        let price = this.lst_price + (price_extra || 0);
        const rule = rules.find((rule) => !rule.min_quantity || quantity >= rule.min_quantity);
        if (!rule) {
            return price;
        }

        if (rule.base === "pricelist") {
            const base_pricelist = this.pos.pricelists.find(
                (pricelist) => pricelist.id === rule.base_pricelist_id[0]
            );
            if (base_pricelist) {
                price = this.get_price(base_pricelist, quantity, 0, true);
            }
        } else if (rule.base === "standard_price") {
            price = this.standard_price;
        }

        if (rule.compute_price === "fixed") {
            price = rule.fixed_price;
        } else if (rule.compute_price === "percentage") {
            price = price - price * (rule.percent_price / 100);
        } else {
            var price_limit = price;
            price -= price * (rule.price_discount / 100);
            if (rule.price_round) {
                price = round_pr(price, rule.price_round);
            }
            if (rule.price_surcharge) {
                price += rule.price_surcharge;
            }
            if (rule.price_min_margin) {
                price = Math.max(price, price_limit + rule.price_min_margin);
            }
            if (rule.price_max_margin) {
                price = Math.min(price, price_limit + rule.price_max_margin);
            }
        }

        // This return value has to be rounded with round_di before
        // being used further. Note that this cannot happen here,
        // because it would cause inconsistencies with the backend for
        // pricelist that have base == 'pricelist'.
        return price;
    }
});

patch(Payment.prototype, {
    export_as_JSON() {
        return {
            name: serializeDateTime(moment().format('jYYYY-jMM-jDD HH:mm:ss')),
            payment_method_id: this.payment_method.id,
            amount: this.get_amount(),
            payment_status: this.payment_status,
            can_be_reversed: this.can_be_reversed,
            ticket: this.ticket,
            card_type: this.card_type,
            cardholder_name: this.cardholder_name,
            transaction_id: this.transaction_id,
        };
    }
});

