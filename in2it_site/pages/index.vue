<template>
	<div>
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