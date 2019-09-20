<template>
	<div>
		<h1 class="landing-page-title">Let's get into it!</h1>
		<p class="landing-page-tagline">In2it is here to help you make an impact in your (neighborhood, city, block) community.</p>
		<p class="landing-page-tagline">Find ways to get involved, contribute your skills, make a difference.</p>
		<filters @filterApplied="updateEvents()"></filters>

		<div class="landing-page-image-row row justify-content-center">
			<img class="landing-page-image" src="/img/landing-page-left.jpg">
			<img class="landing-page-image" src="/img/landing-page-right.png">
		</div>
	</div>
</template>

<script lang='ts'>
	import Filters from '~/components/Filters.vue';

	export default {
		methods: {
			updateEvents: function() {
				this.$router.push('/events');
			}
		},
		components: {
			Filters
		}
	};
</script>