/** @odoo-module **/

import { registry } from "@web/core/registry";
import { loadJS, loadCSS } from "@web/core/assets"
import { _t } from "@web/core/l10n/translation";
import { useInputField } from "@web/views/fields/input_field_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, onWillStart, onMounted } from "@odoo/owl";

export class SHPDateTimeField extends Component {
    static template = "shp.SHPDateTimeField";
    static props = {
        ...standardFieldProps,
        hasTime: {type:Boolean, optional:false},
    };

    setup() {
        
        useInputField({ getValue: () => this.props.record.data[this.props.name] || "" });

        onWillStart(async()=> {
            
            await loadJS('shp/static/src/lib/jalalidatepicker.min.js');
            await loadCSS('shp/static/src/lib/jalalidatepicker.min.css');
            // await loadJS('shp/static/src/lib/jalaali.js');
            // await loadJS('shp/static/src/lib/farvardin.js');
            
        })

        onMounted(()=>{
            jalaliDatepicker.startWatch({
                time: this.props.hasTime,
                hideAfterChange: true,
                autoShow: true,
                zIndex: 10000000,
                separatorChars: {
                    date: '-'
                }
            });
            
        })

        
    }

    triggerIsDirty(isDirty) {
        this.props.record.model.bus.trigger(
            "FIELD_IS_DIRTY",
            isDirty ?? !areDatesEqual(this.getRecordValue(), this.state.value)
        );
    }

    onInput() {
        jalaliDatepicker.updateOptions({
            time: this.props.hasTime,
            hideAfterChange: true
        });
        this.triggerIsDirty(true);
    }

    onBlur(e){
        jalaliDatepicker.updateOptions({
            time: this.props.hasTime,
            hideAfterChange: true
        });
        if (e.target.value){
            //const date = DateTime.fromFormat(e.target.value, "YYYY/MM/DD H:m")
            //console.log(date)
            //this.props.update(date);

            
        }else{
            //if (this.props.value) this.props.update("False")
        }
    }
}

export const shpDateTimeField = {
    component: SHPDateTimeField,
    displayName: "Choose Date",
    supportedTypes: ["date", "datetime"],
    extractProps: ({ attrs }) => ({
        placeholder: attrs.placeholder,
        hasTime: attrs.hasTime,
    }),
};

registry.category("fields").add("shpDateTime", shpDateTimeField);