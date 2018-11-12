<template>
	<div>
		/*This is still pretty rough and not fleshed out, just a rough placeholder for the moment, until we get some proper categories and various options up. Still needs label tags*/
		<filters></filters>
		<resources></resources>
	</div>
</template>

<script>
	import Filters from '~/components/Filters';
	import Resources from '~/components/Resources';

	export default{
		components:{
			Filters,
			Resources
		}
	};
</script>