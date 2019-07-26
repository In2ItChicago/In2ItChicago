<template>
	<div>
		<b-row class="mt-4 mb-2">	
			<b-col>
				<h1 class="event-page-heading">{{ event.title }}</h1>
			</b-col>
		</b-row>
		<b-row>	
			<b-col>
				<p class="event-info-label">Description</p>
				<p>{{ event.description }}</p>

				<p class="event-info-label">Hosted By</p>
				<p class="event-organization">
					{{ event.organization }}
				</p>
				<a class="original-event-link" :href="event.url" target="_blank">Find out more</a>
			</b-col>
			<b-col>
				<p class="event-info-label">Date And Time</p>
				<p class="event-date">{{ event.startDate }}</p>
				<p class="event-time">{{ event.startTime }}</p>

				<p class="event-info-label">Location</p>
				<p class="event-address">{{ event.address }}</p>

				<iframe width="600" height="450" frameborder="0" style="border:0" :src=mapUrl allowfullscreen></iframe>
			</b-col>
		</b-row>
	</div>
</template>


<script>
    export default{
        data() {
			return {
				event: this.$store.activeEvent
			};
		},
		computed: {
			mapUrl: function() {
				return 'https://www.google.com/maps/embed/v1/place?key=AIzaSyDKuKo2WRNv5IhKm_At8wGfD4T142laung&q=' + this.event.address;
			}
		},
		asyncData({redirect, store}) {
			if(store.activeEvent == null) {
				redirect('/');
			}
		}
    };
</script>