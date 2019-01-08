<template>
	<div class="list-group">
		<a :href="eventUrl" class="list-group-item">
			<h4 class="list-group-item-heading">{{ event.title }}</h4>
			<b><p class="list-group-item-text">{{ event.start_date }}</p></b><br>
			<p class="list-group-item-text">{{ event.description }}</p>

			<section class="sharing-saving"><a href=""><img src="images/fb_sm.jpg"></a><a href=""><img src="Images/g+_sm.jpg"></a><a href=""><img src="Images/ln_sm.jpg"></a><a href=""><img src="Images/pnt_sm.jpg"></a><a href=""><img src="Images/ttr_sm.jpg"></a></section>

			<div class="mapLink">
                <a href="">Find on Map</a>
            </div>
		</a>
	</div>
</template>

<script>
    export default {
        props: ['event'],
        computed: {
            eventUrl: function() {
                return '/events/' + this.event.id;
            },
        },
    };
</script>