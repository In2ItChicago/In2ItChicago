<template>
    <div id="map" class="event-map"></div>
</template>

<script>
    export default {
        props: ['events', 'hoveringEventId'],
        data() {
            return {
                markers: [],
                map: null
            };
        },
        mounted() {
            this.createMap();
            this.createMarkers();
            this.fillMap();
        },
        methods: {
            createMap: function() {
                this.map = new google.maps.Map(document.getElementById("map"), {
                    center: { lat: 41.925, lng: -87.68 },
                    zoom: 12
                });
            },
            createMarkers: function() {
                for(let i in this.events){
                    let image = {
                        url: "/img/event-marker-unselected.svg",
                        size: new google.maps.Size(35, 50),
                    };

                    let marker = new google.maps.Marker({
                        position: {lat: this.events[i].lat, lng: this.events[i].lon},
                        icon: image,
                        title: this.events[i].title + ' | ' + this.events[i].address
                    });

                    marker.id = this.events[i].id;

                    let infoContent = 
                        "<h1>" + this.events[i].title + "</h1>" +
                        "<h2>" + this.events[i].address + "</h2>" +
                        "<h3>" + this.events[i].startTime + "</h3>" +
                        "<p>" + this.events[i].description + "</p>";

                    let infowindow = new google.maps.InfoWindow({
                        content: infoContent
                    });

                    marker.addListener('click', function() {
                        infowindow.open(map, marker);
                    });

                    this.markers.push(marker);
                }
            },
            fillMap: function() {
                for(let i in this.markers){
                   this.markers[i].setMap(this.map);
                }
            },
            clearMarkers: function() {
                for(let i in this.markers){
                    this.markers[i].setMap(null);
                }
                this.markers = [];
            }
        },
        watch: {
            events: function() {
                this.clearMarkers();
                this.createMarkers();
                this.fillMap();
            },
            hoveringEventId: function (id) {
                for(let i in this.markers){
                    let image = {
                        url : (this.markers[i].id == id) ? "/img/event-marker-selected.svg" : "/img/event-marker-unselected.svg",
                        size: new google.maps.Size(35, 50)
                    };
                    this.markers[i].setIcon(image);
                }
            }
        }
    }
</script>