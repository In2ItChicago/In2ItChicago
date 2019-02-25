<template>
    <a :href="eventUrl" class="event-summary-link">
        <div class="event-summary d-flex flex-row">
            <div class="d-flex flex-column">
                <div class="d-flex w-100">
                    <h2 class="event-summary-heading mb-1">{{ event.title }}</h2>
                </div>
                <p class="event-summary-description mb-1">{{ event.description }}</p>
            </div>

            <div class="d-flex flex-column">
                <img class="map-icon" src="/img/map-icon.png"/>
                <img class="calendar-icon" src="/img/calendar-icon.png"/>
            </div>
        </div> 
    </a>
</template>

<script>
	export default {
        props: ['event'],
        computed: {
            eventUrl: function() {
                return '/events/' + this.event.id;
            },
        },
    };
</script>