<template>
    <v-card class="event-card" @click="clickOnEvent()">
        <v-card-title class="headline event-card-title">{{ title }}</v-card-title>
        <v-card-subtitle class="event-card-subtitle">{{ event.startDate }} {{ formattedTime }} | {{ event.address }}</v-card-subtitle>
        <v-card-subtitle class="event-card-subtitle">{{ event.organization }}</v-card-subtitle>
        <v-card-text class="event-card-description">{{ description }}</v-card-text>
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
            formattedTime: function() {
                let timeStringPieces = this.event.startTime.split(' ');
                let timePieces = timeStringPieces[0].split(':');
                return timePieces[0] + ':' + timePieces[1] + ' ' + timeStringPieces[1];
            },
            description: function() {
                if(this.event.description.length > 180) {
                    return this.event.description.substr(0, 180) + '...';
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

<style scoped>
    .event-card {
        color: #fff !important;
        margin: 10px;
        cursor: pointer;
        background-color: #287696;
    }
    .event-card:hover {
        background-color: #4ec0c5;
    }
    .event-card-title {
        color: #fff !important;
        font-size: 28px;
        word-break: normal;
    }
    .event-card-subtitle {
        color: #fff !important;
        padding: 10px 18px 5px 18px;
        font-size: 22px;
    }
    .event-card-description {
        margin-top: 10px;
        color: #fff !important;
        font-size: 16px;
    }
</style>