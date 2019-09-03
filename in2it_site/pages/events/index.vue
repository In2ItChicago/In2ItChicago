<template>
    <div>
		<filters @filterApplied="updateEvents()"></filters>
		<event-list :events="events"></event-list>
		
		<no-ssr>
			<notifications group="default"/>
		</no-ssr>
	</div>	
</template>

<script lang='ts'>
	import axios from 'axios';
	import Filters from '~/components/Filters.vue';
	import EventList from '~/components/EventList.vue';
	
	import { dummyData } from '~/store/dummyData.js';
	
	function getEventURL(in2itApiUrl) {
		const eventURL = process.server ? 'event_service:5000' : in2itApiUrl;
		return `http://${eventURL}/events`;
	}

	export default {
		data() {
			return {
				events: [],
			};
		},
		asyncData ({ app, params }) {
            //Ensure get request goes to an endpoint that returns an array or json object
            //If a regular HTML page is returned, the v-for in the view above will try to
            //render each character in the HTML page string as a separate event and nuxt
			//will run out of memory
            if (process.env.DUMMY_DATA) {
                return { events: dummyData };
			}

			return axios.get(getEventURL(app.$env.IN2IT_API_URL))
				.then(res => {
					return { events: res.data };
				});
		},
		methods: {
			updateEvents: function() {
				// Manually set the time to 11:59 PM for now because we don't have a time picker yet
				this.$store.searchFilter.endDate.setHours(23, 59, 59);

				return axios.get(getEventURL(this.$env.IN2IT_API_URL), {
					params: {
						startTime: this.$store.searchFilter.startDate, 
						endTime: this.$store.searchFilter.endDate,
						miles: this.$store.searchFilter.searchRadius,
						address: this.$store.searchFilter.addressOrZip,
						organization: this.$store.searchFilter.organization,
						neighborhood: this.$store.searchFilter.neighborhood
					}
				})
				.then((res) => {
					this.events = res.data;

					this.$notify({
						group: 'default',
						title: 'Filters applied',
						type: 'success'
					});
				})
				.catch((res) => {
					this.$notify({
						group: 'default',
						title: 'Error applying filters',
						type: 'error'
					});
				});
			}
		},
		components: {
			Filters,
			EventList
		}
	};
</script>