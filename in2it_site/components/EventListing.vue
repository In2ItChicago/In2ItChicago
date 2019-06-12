<template>
    <div @click="navigateToEventPage()" class="event-listing d-flex flex-row event-listing-link">
        <div class="d-flex flex-column">
            <div class="d-flex w-100">
                <h2 class="event-listing-title mb-1">{{ event.title }}</h2>
            </div>
            <div class="d-flex w-100">
                <h3 class="event-listing-time-location mb-1">{{ event.start_date }} {{ event.start_time  }}, {{ event.address }}</h3>
            </div>
            <p class="event-listing-description mb-1">{{ event.description }}</p>
        </div>

        <div class="d-flex flex-column">
            <img class="map-icon" src="/img/map-icon.png"/>
            <img class="calendar-icon" src="/img/calendar-icon.png"/>
        </div>
    </div> 
</template>

<script>
	export default {
        props: ['event'],
        methods: {
            navigateToEventPage: function() {
                this.$store.activeEvent = this.event;
                this.$router.push({path: '/events/' + this.event.id});
            }
        },
    };
</script>