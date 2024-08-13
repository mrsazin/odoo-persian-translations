/** @odoo-module **/

import { registry } from "@web/core/registry"
import { loadJS, loadCSS } from "@web/core/assets"
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useInputField } from "@web/views/fields/input_field_hook";
import { Component, useRef, onWillStart, onMounted, useState } from "@odoo/owl";
const { DateTime } = luxon;

export class PDateTime extends Component{
    static props = { ...standardFieldProps,
        onChange: Function
    };

    setup(){
        console.log('setup');
        //const pDateTimeHook= useInputField({});
        this.divRef = useRef("div");
        this.state = useState(pDateTime.state);

        onWillStart(async()=> {
            console.log('before will');
            await loadJS('shp/static/src/lib/jalalidatepicker.min.js')
            await loadCSS('shp/static/src/lib/jalalidatepicker.min.css');
            console.log('after will');
        })

        onMounted(()=>{
            console.log('before mount');
            jalaliDatepicker.startWatch({
                time: true,
                hideAfterChange: true
            });

            console.log('after mount');
        })
    }

    onBlur(e){
        console.log("onBlur");
        console.log(e.target.value);
        //this.props.componentDidUpdate();
        if (e.target.value){
            //const date = DateTime.fromFormat(e.target.value, "dd/MM/yyyy")
            //this.props.update(date);
            //this.props.value = date
            //e.target.value = date
            // this.props.update(date)
            // this.props.update(e.target.value)
        }else{
            //if (this.props.value) this.props.update("False")
        }
    }

    onChange(e){
        console.log("onChange");
        console.log(e.target.value);
        if (e.target.value){
            const date = DateTime.fromFormat(e.target.value, "dd/MM/yyyy")
            this.props.record.update(date);
            //this.props.update(date);
            //this.props.value = date
            //e.target.value = date
            // this.props.update(date)
            // this.props.update(e.target.value)
        }else{
            //if (this.props.value) this.props.update("False")
        }        
    }

    // updateRecord(value) {
    //     console.log(value);
    //     // const changes = { [this.props.name]: value };
    //     // if (this.props.update) {
    //     //     return this.props.update(changes);
    //     // }
    //     // return this.props.record.update(changes);
    // }

    get formattedValue(){
        //return this.props.value ? this.props.value.toFormat("dd/MM/yyyy"): ""
    }
}

PDateTime.template = "shp.PDateTime"

PDateTime.displayName = "Date Shamsi Field"

export const pDateTime = {
    component: PDateTime,
    supportedTypes: ["date", "datetime"],
};

registry.category("fields").add("pdatetime", pDateTime);

