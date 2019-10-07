<template>
    <div @mouseover="hoverOnEvent()"  @click="clickOnEvent()" class="event-listing d-flex flex-row event-listing-link">
        <div class="d-flex flex-column">
            <div class="d-flex w-100">
                <h2 class="event-listing-title">{{ title }}</h2>
            </div>
            <div class="d-flex w-100">
                <h3 class="event-listing-organization">{{ event.organization }}</h3>
            </div>
            <div class="d-flex w-100">
                <h4 class="event-listing-time-location">{{ event.startDate }} {{ event.startTime  }} | {{ event.address }}</h4>
            </div>
            <p class="event-listing-description">{{ description }}</p>
        </div>
    </div> 
</template>

<script>
	export default {
        props: ['event'],
        computed: {
            title: function() {
                if(this.event.title.length > 50) {
                    return this.event.title.substr(0, 50) + '...';
                }
                return this.event.title;
            },
            description: function() {
                if(this.event.description.length > 140) {
                    return this.event.description.substr(0, 140) + '...';
                }
                return this.event.description;
            }
        },
        methods: {
            hoverOnEvent: function() {
                this.$emit('eventHover', this.event.id);
            },
            clickOnEvent: function() {
                this.$emit('eventClick', this.event.id);
            }
        },
    };
</script>