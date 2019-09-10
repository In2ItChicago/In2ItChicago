<template>
    <div @click="navigateToEventPage()" @mouseover="hoverOnEvent()" class="event-listing d-flex flex-row event-listing-link">
        <div class="d-flex flex-column">
            <div class="d-flex w-100">
                <h2 class="event-listing-title">{{ event.title }}</h2>
            </div>
            <div class="d-flex w-100">
                <h3 class="event-listing-time-location">{{ event.startDate }} {{ event.startTime  }} | {{ event.address }}</h3>
            </div>
            <p class="event-listing-description">{{ description }}</p>
        </div>
    </div> 
</template>

<script>
	export default {
        props: ['event'],
        computed: {
            description: function() {
                if(this.event.description.length > 140){
                    return this.event.description.substr(0, 140) + '...';
                }
                return this.event.description;
            }
        },
        methods: {
            navigateToEventPage: function() {
                this.$store.activeEvent = this.event;
                this.$router.push({path: '/events/' + this.event.id});
            },
            hoverOnEvent: function() {
                this.$emit('eventHover', this.event.id);
            }
        },
    };
</script>