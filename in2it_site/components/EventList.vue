<template>
	<div class="content-row">
		<div class="events-container">
			<div v-if="eventsAvailable">
				<paginate
					:page-count="3"
					:click-handler="paginateHandler"
					:prev-text="'<'"
					:next-text="'>'"
					:container-class="'pagination event-pagination justify-content-center d-flex'"
					:page-class="'event-pagination-item'"
					:prev-class="'event-pagination-prev-item'"
					:next-class="'event-pagination-next-item'">
				</paginate>
				<div v-for="event in events">
					<event-listing :event="event" v-on:eventHover="hoveringEventId = $event" v-on:eventClick="focussedEventId = $event"></event-listing>
				</div>
			</div>
			<div v-else class="no-event-message">
				<span>No events found, try expanding your dates or search radius</span>
			</div>
		</div>
		<div class="map-container">
			<client-only>
				<event-map :events="events" :hoveringEventId="hoveringEventId" :focussedEventId="focussedEventId"></event-map>
			</client-only>
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
				hoveringEventId: null,
				focussedEventId: null
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