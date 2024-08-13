/** @odoo-module **/

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, onWillStart, onMounted } from "@odoo/owl";
//import { DateTime } from luxon;

export class DateHijriField extends Component{
    static props = { ...standardFieldProps };

    setup(){
        console.log('setup');

        onWillStart(async()=> {
            console.log('before will');
            await loadJS('shp/static/src/lib/bootstrap-hijri-datetimepicker.min.js')
            console.log('after will');
        })

        onMounted(()=>{
            console.log('before mount');
            $('#picker').hijriDatePicker({
                hijri: true,
                format: 'YYYY/MM/DD',
                hijriFormat: 'iYYYY/iMM/iDD'
            })

            console.log('after mount');
        })
    }

    onBlur(e){
        if (e.target.value){
            //const date = DateTime.fromFormat(e.target.value, "dd/MM/yyyy")
            //this.props.update(date)
            this.props.update(e.target.value)
        }else{
            this.props.update(false)
        }
    }

    get formattedValue(){
        return this.props.value ? this.props.value.toFormat("dd/MM/yyyy"): ""
    }
}

DateHijriField.template = "shp.DateHijriField"
// DateHijriField.props = {
//     ...standardFieldProps
// }

DateHijriField.displayName = "Date Hijri Field"
// DateHijriField.supportedTypes =["date"]

export const dateHijriField = {
    component: DateHijriField,
    supportedTypes: ["date"],
};

// registry.category("fields").add("date_hijri", DateHijriField)
registry.category("fields").add("date_hijri", dateHijriField);

