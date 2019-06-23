import Vue from 'vue'
import Datepicker from 'vuejs-datepicker'

const VueDatepicker = {
    install(Vue,options) {
        Vue.component('datepicker', Datepicker)
    }
}
Vue.use(VueDatepicker);

export default VueDatepicker;