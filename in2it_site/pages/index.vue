<template>
	<div>
		<page-title></page-title>
		<filters @filterApplied="updateEvents()"></filters>

		<div class="landing-page-image-row row justify-content-center">
			<img class="landing-page-image" src="/img/landing-page-left.jpg">
			<img class="landing-page-image" src="/img/landing-page-right.png">
		</div>
	</div>
</template>

<script lang='ts'>
	import Filters from '~/components/Filters.vue';
	import PageTitle from '~/components/PageTitle.vue';

	export default {
		methods: {
			updateEvents: function() {
				this.$router.push('/events');
			}
		},
		components: {
			Filters,
			PageTitle
		}
	};
</script>