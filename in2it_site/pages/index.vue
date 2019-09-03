<template>
	<div>
		<div class="landing-page-content">
			<h1 class="landing-page-title">Let's get into it!</h1>
			<p class="landing-page-text">
				A survey of our fellow Chicagoans found that there is a sizeable group that wants to be civically engaged, but faces obstacles to doing so. We want to make it easier for people to get involved in their communities.
			</p>
			<p class="landing-page-text">
				Check out our list of community events so you can start making a difference!
			</p>
		</div>
		<filters @filterApplied="updateEvents()"></filters>
	</div>
</template>

<script lang='ts'>
	import Filters from '~/components/Filters.vue';

	export default {
		methods: {
			updateEvents: function() {
				
			}
		},
		components: {
			Filters
		}
	};
</script>