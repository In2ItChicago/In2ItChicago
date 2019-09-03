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
			return axios.get(getEventURL(app.$env.IN2IT_API_URL))
				.then(res => {
					return { events: res.data };
				});
		},
		mounted() {
			this.updateEvents();
		},
		methods: {
			updateEvents: function() {
				return axios.get(getEventURL(this.$env.IN2IT_API_URL), {
					params: {
						startTime: this.$store.state.searchFilter.startDate, 
						endTime: this.$store.state.searchFilter.endDate,
						miles: this.$store.state.searchFilter.searchRadius,
						address: this.$store.state.searchFilter.addressOrZip,
						organization: this.$store.state.searchFilter.organization,
						neighborhood: this.$store.state.searchFilter.neighborhood
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