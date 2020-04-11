<template>
  <div class="site">
      <v-alert prominent class="covid-alert">
        <v-row align="center">
          <v-col class="d-flex flex-row">
            <v-icon>
              mdi-alert-circle
            </v-icon>
            <div class="covid-alert-text">
              To help in the fight against COVID-19, we recommend avoiding in-person civic activities. Instead, consider the <a href="/get-involved-from-home">following projects</a> where you can get involved from home.
            </div>
            <v-btn class="d-flex get-involved-btn" href="/get-involved-from-home">
              Get Involved From Home
            </v-btn>
          </v-col>
        </v-row>
      </v-alert>
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

<style scoped>
  .covid-alert{
    color: #ff5252 !important;
    background-color: #ffe9eb;
  }

  .covid-alert-text{
    font-size: 20px;
    margin-left:10px;
  }

  .covid-alert i {
    color: red;
  }

  .get-involved-btn{
    display:flex;
    margin-left:auto;
  }

  .get-involved-btn:hover{
    text-decoration: none;
  }
</style>