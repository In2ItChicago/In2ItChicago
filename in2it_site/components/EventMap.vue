<template>
    <div id="map" class="event-map"></div>
</template>

<script>
    export default {
        props: ['events', 'hoveringEventId', 'focusedEventId'],
        data() {
            return {
                markers: [],
                map: null,
                activeMarker: null,
                center: {
                    lat: 41.88324258145789,
                    lng: -87.63241624252306
                }
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
                    center: this.center,
                    zoom: 14
                });
            },
            createMarkers: function() {
                const events = this.events;
                for (let i in events) {
                    let latLng = {lat: events[i].lat, lng: events[i].lon};

                    //Skip creating markers for events without a valid latLng
                    if(latLng.lat == null || latLng.lng == null) continue;

                    let image = {
                        url: "/img/event-marker-unselected.svg",
                        size: new google.maps.Size(35, 50),
                    };

                    let marker = new google.maps.Marker({
                        position: latLng,
                        icon: image,
                        title: events[i].title + ' | ' + events[i].address
                    });

                    marker.id = events[i].id;
                    marker.latLng = latLng;

                    let infoContent = 
                        "<h2>" + events[i].title + "</h2>" +
                        "<h4>" + events[i].address + "</h4>" +
                        "<h4>" + events[i].startDate + ' ' + this.getFormattedTime(events[i].startTime) + "</h4>" +
                        "<p class='event-marker-description'>" + events[i].description + "</p>" +
                        "<a class='event-marker-link' href=" + events[i].url + " target=" + "_blank" + ">" + "Visit event site" + "<img class='event-marker-outgoing-link-icon' src='https://img.icons8.com/metro/26/000000/external-link.png'></a>";

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
            closeActiveMarker: function() {
                if (this.activeMarker) {
                    this.activeMarker.infoWindow.close();
                }
            },
            setActiveMarker: function(marker) {
                this.closeActiveMarker();
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

                //Default center is Chicago Loop
                let center = this.center;

                let latSum = 0;
                let lonSum = 0;
                for (let i in this.markers){
                    latSum += this.markers[i].latLng.lat;
                    lonSum += this.markers[i].latLng.lng;
                }

                if(latSum > 0 && lonSum > 0){
                    center.lat = latSum / this.markers.length;
                    center.lng = lonSum / this.markers.length;
                }

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
            updateMarkerFocusState: function(focusedEventId) {
                if (!this.$google)  return;
                for (let i in this.markers) {
                    let image = {
                        url : (this.markers[i].id == focusedEventId) ? "/img/event-marker-selected.svg" : "/img/event-marker-unselected.svg",
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
            focusedEventId: function (id) {
                if (!this.$google) return;
                this.closeActiveMarker();
                for (let i in this.markers) {
                    if (this.markers[i].id != id) continue;
                    this.setActiveMarker(this.markers[i]);
                    this.centerMapOnMarker(this.markers[i]);
                }
            }
        }
    }
</script>