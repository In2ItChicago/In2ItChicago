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
				return axios.get(this.eventUrl, {
					params: this.$store.state.searchFilter
				})
				.then((res) => {
					this.events = res.data;
				});
			}
		},
		computed: {
			eventUrl: function() {
				const eventURL = process.server ? 'http://event_service:5000' : this.$env.IN2IT_API_URL;
				return `${eventURL}/events`;
			}
		},
		components: {
			Filters,
			EventList
		}
	};
</script>