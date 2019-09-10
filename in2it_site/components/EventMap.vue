<template>
    <div id="map" class="event-map"></div>
</template>

<script>
    export default {
        props: ['events'],
        mounted() {
            let latLong = { lat: 41.925, lng: -87.68 };
            const map = new google.maps.Map(document.getElementById("map"), {
                center: latLong,
                zoom: 12
            });
            
            for(let i in this.events){
                let infoContent = 
                    "<h1>" + this.events[i].title + "</h1>" +
                    "<h2>" + this.events[i].address + "</h2>" +
                    "<h3>" + this.events[i].startTime + "</h3>" +
                    "<p>" + this.events[i].description + "</p>";

                let infowindow = new google.maps.InfoWindow({
                    content: infoContent
                });

                let marker = new google.maps.Marker({
                    position: {lat: this.events[i].lat, lng: this.events[i].lon},
                    map: map,
                    title: this.events[i].title + ' | ' + this.events[i].address
                });

                marker.addListener('click', function() {
                    infowindow.open(map, marker);
                });
            }
        }
    }
</script>