<template>
	<div>
		<page-title></page-title>
		<filters @filterApplied="updateEvents()"></filters>

		<v-row style="margin-top:-80px;">
			<v-col cols="6">
				<v-img
					src="/img/landing-page-left.jpg"
					max-height="415"
					max-width="620"
					class="ml-auto"
					style="border-radius:8px;"
				></v-img>
			</v-col>
			<v-col cols="6">
				<v-img
					src="/img/landing-page-right.jpg"
					max-height="415"
					max-width="620"
					style="border-radius:8px;"
				></v-img>
			</v-col>
		</v-row>
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