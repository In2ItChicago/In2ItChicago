import Vue from 'vue';
import Notifications from 'vue-notification';

const VueNotifications = {
    install(Vue, options) {
        Vue.component('notifications', Notifications);
    }
}
Vue.use(Notifications);

export default Notifications;