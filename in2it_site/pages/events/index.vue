<template>
    <div>
		<filters @filterApplied="updateEvents()"></filters>
		<event-list :events="events" @paginated="updateEvents()"></event-list>

		<client-only>
			<notifications group="default"/>
		</client-only>
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
				events: []
			};
		},
		mounted() {
			this.updateEvents();
		},
		methods: {
			updateEvents: function() {
				return axios.get(getEventURL(this.$env.IN2IT_API_URL), {
					params: this.$store.state.searchFilter
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