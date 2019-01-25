<template>
	<div class="events">
		<div v-if="eventsAvailable">
			<div v-for="event in events">
				<event-summary :event="event"></event-summary>
			</div>
		</div>
		<div v-else class="no-event-message">
			<span>No events available, please try again later.</span>
		</div>
	</div>
</template>

<script>
	import EventSummary from '~/components/EventSummary.vue';
	export default{
		props: ['events'],
		computed: {
			eventsAvailable: function() {
				return this.events.length > 0;
			}
		},
		components: {
			EventSummary
		}
	};
</script>