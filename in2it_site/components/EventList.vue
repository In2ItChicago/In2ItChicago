<template>
	<div class="content-row event-map-container">
		<div class="events-container">
			<div v-if="eventsAvailable">
				<paginate
					:page-count="pageCount"
					:click-handler="paginateHandler"
					:prev-text="'<'"
					:next-text="'>'"
					:container-class="'pagination event-pagination justify-content-center d-flex'"
					:page-class="'event-pagination-item'"
					:prev-class="'event-pagination-item'"
					:next-class="'event-pagination-item'">
				</paginate>
				<div v-for="event in eventResult.events">
					<event-listing :event="event" v-on:eventHover="hoveringEventId = $event" v-on:eventClick="focusedEventId = $event"></event-listing>
				</div>
			</div>
			<div v-else class="no-event-message">
				<span>No events found, try expanding your dates or search radius</span>
			</div>
		</div>
		<div class="map-container">
			<client-only>
				<event-map :events="eventResult.events" :hoveringEventId="hoveringEventId" :focusedEventId="focusedEventId"></event-map>
			</client-only>
		</div>
	</div>
</template>

<script>
	import EventMap from '~/components/EventMap.vue';
	import EventListing from '~/components/EventListing.vue';
	export default{
		props: ['eventResult'],
		data() {
			return {
				hoveringEventId: null,
				focusedEventId: null
			};
		},
		computed: {
			eventsAvailable: function() {
				if (!this.eventResult.events) {
					return false;
				}
				return this.eventResult.events.length > 0;
			},
			pageCount: function() {
				if (this.eventResult) {
					return Math.ceil(this.eventResult.totalCount / 4);
				}
				return 3;
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

<style scoped>
	@media (max-width: 768px) {
        .event-map-container{
			display: flex;
			flex-direction: column;
		}

		.events-container{
			width:100%;
		}

		.map-container{
			width:100vw;
			height:50vh;
		}

		.event-map{
			width:100vw;
			height:50vh;
		}
    }
</style>