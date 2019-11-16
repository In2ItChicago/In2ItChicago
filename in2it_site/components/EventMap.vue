<template>
    <div id="map" class="event-map"></div>
</template>

<script>
    export default {
        props: ['events', 'hoveringEventId', 'focussedEventId'],
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
                this.centerMapOnVisibleMarkers();
            },
            createMap: function() {
                this.map = new google.maps.Map(document.getElementById("map"), {
                    center: { lat: 41.925, lng: -87.68 },
                    zoom: 14
                });
            },
            createMarkers: function() {
                for (let i in this.events) {
                    let image = {
                        url: "/img/event-marker-unselected.svg",
                        size: new google.maps.Size(35, 50),
                    };

                    let latLng = {lat: this.events[i].lat, lng: this.events[i].lon};

                    let marker = new google.maps.Marker({
                        position: latLng,
                        icon: image,
                        title: this.events[i].title + ' | ' + this.events[i].address
                    });

                    marker.id = this.events[i].id;
                    marker.latLng = latLng;

                    let infoContent = 
                        "<h2>" + this.events[i].title + "</h2>" +
                        "<h4>" + this.events[i].address + "</h4>" +
                        "<h4>" + this.getFormattedTime(this.events[i].startTime) + "</h4>" +
                        "<p class='event-marker-description'>" + this.events[i].description + "</p>" +
                        "<a class='event-marker-link' href=" + this.events[i].url + " target=" + "_blank" + ">" + "Visit event site" + "<img class='event-marker-outgoing-link-icon' src='https://img.icons8.com/metro/26/000000/external-link.png'></a>";

                    let infoWindow = new google.maps.InfoWindow({
                        content: infoContent
                    });

                    const instance = this;
                    marker.addListener('click', function() {
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
                this.updateMarkerFocusState(this.activeMarker.id);
                this.activeMarker.infoWindow.open(this.map, this.activeMarker);
            },
            addMarkersToMap: function() {
                for (let i in this.markers) {
                   this.markers[i].setMap(this.map);
                }
            },
            centerMapOnMarker: function(marker) {
                let lat = marker.latLng.lat;
                let lng = marker.latLng.lng;
                this.map.setCenter({lat, lng});
            },
            centerMapOnVisibleMarkers: function() {
                if(this.markers.length <= 0) return;

                let latSum = 0;
                let lonSum = 0;
                for (let i in this.markers){
                    latSum += this.markers[i].latLng.lat;
                    lonSum += this.markers[i].latLng.lng;
                }

                let center = {
                    lat: latSum / this.markers.length,
                    lng: lonSum / this.markers.length
                };

                this.map.setCenter(center);
            },
            clearMarkers: function() {
                for (let i in this.markers) {
                    this.markers[i].setMap(null);
                }
                this.markers = [];
            },
            getFormattedTime: function(timeString) {
                let timeStringPieces = timeString.split(' ');
                let timePieces = timeStringPieces[0].split(':');
                return timePieces[0] + ':' + timePieces[1] + ' ' + timeStringPieces[1];
            },
            updateMarkerFocusState: function(focussedEventId) {
                if (!this.$google)  return;
                for (let i in this.markers) {
                    let image = {
                        url : (this.markers[i].id == focussedEventId) ? "/img/event-marker-selected.svg" : "/img/event-marker-unselected.svg",
                        size: new google.maps.Size(35, 50)
                    };
                    this.markers[i].setIcon(image);
                }
            }
        },
        watch: {
            events: function() {
                this.clearMarkers();
                this.initMap();
            },
            hoveringEventId: function (id) {
                this.updateMarkerFocusState(id);
            },
            focussedEventId: function (id) {
                if (!this.$google)  return;
                for (let i in this.markers) {
                    if (this.markers[i].id != id) continue;
                    this.setActiveMarker(this.markers[i]);
                    this.centerMapOnMarker(this.markers[i]);
                }
            }
        }
    }
</script>