<template>
	<div>
		<div class="content-row">
			<filters @filterApplied="updateEvents()"></filters>
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
	import { Service } from 'feathersjs__feathers';
	
	import { dummyData } from '~/store/dummyData.js';
	
	function getClient(url: string): Service<any> {
		const app = feathers();
		const restClient = rest('http://' + url);
		app.configure(restClient.axios(axios));
		return app.service('events');
	}

	const eventServiceClient = getClient(process.env.API_URL || '');

	export default {
		data() {
			return {
				events: [],
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
			const eventService = getClient('event_service:5000');
			return eventService.find({query: {}})
				.then(res => {
					return { events: res };
				});
		},
		methods: {
			updateEvents: function() {
				return eventServiceClient.find({
					query: {
						start_timestamp: this.$store.searchFilter.startDate, 
						end_timestamp: this.$store.searchFilter.endDate,
						miles: this.$store.searchFilter.searchRadius,
						address: this.$store.searchFilter.addressOrZip || '60611'
					}
				})
				.then((res) => {
					this.events = res;
				});
			}
		},
		components: {
			Filters,
			EventList
		}
	};
</script>
