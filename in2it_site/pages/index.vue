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

	export default {
		data() {
			return {
				events: [],
			};
		},
		asyncData ({ app, params }) {
			const eventURL = process.server ? 'event_service:5000' : app.$env.IN2IT_API_URL;
            //Ensure get request goes to an endpoint that returns an array or json object
            //If a regular HTML page is returned, the v-for in the view above will try to
            //render each character in the HTML page string as a separate event and nuxt
			//will run out of memory
            if (process.env.DUMMY_DATA) {
                return { events: dummyData };
			}
			const eventService = getClient(eventURL);
			return eventService.find({query: {}})
				.then(res => {
					return { events: res };
				});
		},
		methods: {
			updateEvents: function() {
				const eventServiceClient = getClient(this.$env.IN2IT_API_URL || '');

				// Manually set the time to 11:59 PM for now because we don't have a time picker yet
				this.$store.searchFilter.endDate.setHours(23, 59, 59);
				return eventServiceClient.find({
					query: {
						startTime: this.$store.searchFilter.startDate, 
						endTime: this.$store.searchFilter.endDate,
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
