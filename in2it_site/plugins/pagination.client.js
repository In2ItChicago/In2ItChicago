import Vue from 'vue';
import Paginate from 'vuejs-paginate/src/components/Paginate.vue';

const VuePaginate = {
	install(Vue, options){
		Vue.component('paginate', Paginate)
	}
}

Vue.use(VuePaginate)

export default VuePaginate;