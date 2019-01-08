<template>
	<section class="container">
		<h2>Event Results</h2>
		<div v-if="eventsAvailable">
			<div v-for="event in events">
				<event-listing :event="event"></event-listing>
			</div>
		</div>
		<div v-else>
			<span>No events available, please try again later.</span>
		</div>
	</section>
</template>

<script>
	import EventListing from '~/components/EventListing';

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