<template>
    <div id="map" class="event-map"></div>
</template>

<script>
    export default {
        props: ['events', 'hoveringEventId'],
        data() {
            return {
                markers: [],
                map: null,
                activeMarker: null
            };
        },
        mounted() {
            this.initMap();
        },
        methods: {
            initMap: function() {
                if (this.$google) {
                    this.renderMap();
                }
                else {
                    const callback = () => {
                        this.renderMap();
                        window.removeEventListener('maps-module:loaded', callback);
                    }
                    window.addEventListener('maps-module:loaded', callback);
                }
            },
            renderMap: function() {
                this.createMap();
                this.createMarkers();
                this.addMarkersToMap();
            },
            createMap: function() {
                this.map = new google.maps.Map(document.getElementById("map"), {
                    center: { lat: 41.925, lng: -87.68 },
                    zoom: 12
                });
            },
            createMarkers: function() {
                for (let i in this.events) {
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
                        "<h2>" + this.events[i].title + "</h2>" +
                        "<h4>" + this.events[i].address + "</h4>" +
                        "<h4>" + this.events[i].startTime + "</h4>" +
                        "<p>" + this.events[i].description + "</p>" +
                        "<a href=" + this.events[i].url + " target=" + "_blank" + ">" + "Find out more" + "</a>";

                    let infoWindow = new google.maps.InfoWindow({
                        content: infoContent
                    });

                    const instance = this;
                    marker.addListener('click', function() {
                        infoWindow.open(map, marker);
                        instance.setActiveMarker(marker);
                    });

                    marker.infoWindow = infoWindow;

                    this.markers.push(marker);
                }
            },
            setActiveMarker: function(marker) {
                if (this.activeMarker) {
                    this.activeMarker.infoWindow.close();
                }
                this.activeMarker = marker;
            },
            addMarkersToMap: function() {
                for (let i in this.markers) {
                   this.markers[i].setMap(this.map);
                }
            },
            clearMarkers: function() {
                for (let i in this.markers) {
                    this.markers[i].setMap(null);
                }
                this.markers = [];
            }
        },
        watch: {
            events: function() {
                this.clearMarkers();
                this.initMap();
            },
            hoveringEventId: function (id) {
                if (!this.$google)  return;
                for (let i in this.markers) {
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