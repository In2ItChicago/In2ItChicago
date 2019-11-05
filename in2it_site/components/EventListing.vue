<template>
    <v-card nuxt color="#eceff1" :elevation="24" @mouseover="hoverOnEvent()"  @click="clickOnEvent()" class="event-listing event-listing-link">
        <v-card-title class="headline" style="color: #173450">{{ title }}</v-card-title>
        <div class="d-flex flex-column">
            <div class="d-flex w-100">
                <v-card-subtitle style= "color: #0D47A1"> {{ event.organization }} </v-card-subtitle>
            </div>
            <div class="d-flex w-100">
                <v-card-text style="color: #212121">{{ event.startDate }} {{ event.startTime  }} | {{ event.address }}</v-card-text>
            </div>
            <v-card-text class="d-none d-md-block" style="color: #212121">{{ description }}</v-card-text>
        </div>
    </v-card> 
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