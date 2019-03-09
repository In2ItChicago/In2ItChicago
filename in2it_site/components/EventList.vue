<template>
	<div class="events">
		<div v-if="eventsAvailable">
			<div v-for="event in events">
				<event-listing :event="event"></event-listing>
			</div>
		</div>
		<div v-else class="no-event-message">
			<span>No events available, please adjust your search filter.</span>
		</div>
	</div>
</template>

<script>
	import EventListing from '~/components/EventListing.vue';
	export default{
		props: ['events'],
		computed: {
			eventsAvailable: function() {
				return this.events.length > 0;
			}
		},
		components: {
			EventListing
		}
	};
</script>