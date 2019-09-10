<template>
    <div id="map" class="event-map"></div>
</template>

<script>
    export default {
        mounted() {
            const map = new google.maps.Map(document.getElementById("map"), {
                center: { lat: 41.888423, lng: -87.635072 },
                zoom: 16
            });
            console.log('loaded map');
        }
    }
</script>