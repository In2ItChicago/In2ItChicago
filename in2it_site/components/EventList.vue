<template>
	<div class="content-row">
		<div class="map-container">
			<event-map :events="events"></event-map>
		</div>
		<div class="events-container">
			<div v-if="eventsAvailable">
				<div v-for="event in events">
					<event-listing :event="event"></event-listing>
				</div>
			</div>
			<div v-else class="no-event-message">
				<span>No events available, please adjust your search filter.</span>
			</div>
		</div>
	</div>
</template>

<script>
	import EventMap from '~/components/EventMap.vue';
	import EventListing from '~/components/EventListing.vue';
	export default{
		props: ['events'],
		computed: {
			eventsAvailable: function() {
				return this.events.length > 0;
			}
		},
		components: {
			EventMap,
			EventListing
		}
	};
</script>