<template>
  <div class="site">
      <header>
			  <page-header></page-header>
		  </header>
      <div class="page-container" data-app="true">
        <nuxt/>
      </div>
      <footer>
			  <page-footer></page-footer>
		  </footer>
  </div>
</template>

<script>
  	import PageFooter from '~/components/PageFooter.vue';
    import PageHeader from '~/components/PageHeader.vue';
    
    export default{
      components: {
        PageFooter,
        PageHeader
      }
    };
</script>
