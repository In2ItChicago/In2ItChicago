<template>
	<div>
		<div class="content">
			<filters :searchFilters="searchFilters" @filterApplied="updateEvents()"></filters>
			<event-list :events="events"></event-list>
		</div>
	</div>	
</template>

<script lang='ts'>
	import axios from 'axios';
	import rest from '@feathersjs/rest-client';
	import feathers from '@feathersjs/feathers';
	import Filters from '~/components/Filters.vue';
	import EventList from '~/components/EventList.vue';
	
	import { dummyData } from '~/store/dummyData.js';
	
	function getClient(url) {
		const app = feathers();
		const restClient = rest(url);
		app.configure(restClient.axios(axios));
		return app.service('events');
	}

	const eventServiceClient = getClient(process.env.API_URL);

	export default {
		data() {
			return {
				events: [],
				searchFilters: {
					addressOrZip: '',
					searchRadius: 5,
					startDate: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate()),
					endDate: new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate())
				}
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
			const eventService = getClient('http://event_service:5000');
			return eventService.find({query: {start_timestamp: 0, end_timestamp: 10000000000000}})
				.then(res => {
					return { events: res.data };
				});
		},
		methods: {
			updateEvents: function() {
				return eventServiceClient.find({
					query: {
						start_timestamp: this.searchFilters.startDate.getTime() / 1000, 
						end_timestamp: this.searchFilters.endDate.getTime() / 1000,
						miles: this.searchFilters.searchRadius,
						address: this.searchFilters.addressOrZip
					}
				})
				.then((res) => {
					this.events = res.data;
				});
			}
		},
		components: {
			Filters,
			EventList
		}
	};
</script>
