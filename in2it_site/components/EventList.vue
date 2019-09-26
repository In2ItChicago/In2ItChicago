<template>
	<div class="content-row">
		<div class="map-container">
			<client-only>
				<event-map :events="events" :hoveringEventId="hoveringEventId"></event-map>
			</client-only>
		</div>
		<div class="events-container">
			<div v-if="eventsAvailable">
				<div v-for="event in events">
					<event-listing :event="event" v-on:eventHover="hoveringEventId = $event"></event-listing>
				</div>
				<paginate
					:page-count="8"
					:click-handler="paginateHandler"
					:prev-text="'<'"
					:next-text="'>'"
					:container-class="'pagination event-pagination justify-content-center d-flex'"
					:page-class="'event-pagination-item'"
					:prev-class="'event-pagination-prev-item'"
					:next-class="'event-pagination-next-item'">
				</paginate>
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
		data() {
			return {
				hoveringEventId: null
			};
		},
		computed: {
			eventsAvailable: function() {
				return this.events.length > 0;
			}
		},
		methods: {
			paginateHandler: function(pageNum) {
				this.$store.commit('searchFilter/setOffset', pageNum);
				this.$emit('paginated');
            }
		},
		components: {
			EventMap,
			EventListing
		}
	};
</script>