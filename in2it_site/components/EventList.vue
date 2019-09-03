<template>
	<div class="content-row">
		<div class="events-container" v-if="eventsAvailable">
			<div v-for="event in events">
				<event-listing :event="event"></event-listing>
			</div>
		</div>
		<div v-else class="no-event-message">
			<span>No events available, please adjust your search filter.</span>
		</div>
		<div class="map-container">
			<iframe class="events-map" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/place?key=AIzaSyDKuKo2WRNv5IhKm_At8wGfD4T142laung&q=222 W Merchandise Mart Plaza #470, Chicago, IL 60654" allowfullscreen></iframe>
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