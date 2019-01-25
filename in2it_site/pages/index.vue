<template>
	<div>
		<header>
			<page-header></page-header>
		</header>

		<div class="container">
			<div class="content">
				<filters></filters>
				<event-list :events="events"></event-list>
			</div>
		</div>

		<footer>
			<page-footer></page-footer>
		</footer>
	</div>	
</template>

<script lang='ts'>
	import axios from 'axios';
	import rest from '@feathersjs/rest-client';
	import feathers from '@feathersjs/feathers';
	import Filters from '~/components/Filters.vue';
	import EventList from '~/components/EventList.vue';
	import PageFooter from '~/components/PageFooter.vue';
	import PageHeader from '~/components/PageHeader.vue';
	
    import { dummyData } from '~/store/dummydata.js';

	const app = feathers();
	const restClient = rest('http://event_service:5000');
	app.configure(restClient.axios(axios));
    const events = app.service('events');

	export default {
		data() {
			return {
				events: []
			};
		},
		asyncData ({ params }) {
            //Ensure get request goes to an endpoint that returns an array or json object
            //If a regular HTML page is returned, the v-for in the view above will try to
            //render each character in the HTML page string as a separate event and nuxt
            //will run out of memory
            if (process.env.DUMMY_DATA) {
                return { events: dummyData };
            }
			return events.find({query: {start_timestamp: 0, end_timestamp: 10000000000000}})
				.then(res => {
					return { events: res.data };
				});
		},
		components: {
			Filters,
			EventList,
			PageFooter,
			PageHeader
		}
	};
</script>
