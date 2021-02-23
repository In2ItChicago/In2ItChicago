<template>    
    <v-alert v-if="shouldDisplay" prominent class="covid-alert">
        <v-row align="center">
          <v-col md="10" sm="12" cols="12" class="d-flex">
            <v-icon>
              mdi-alert-circle
            </v-icon>
            <div class="covid-alert-text">
              To help in the fight against COVID-19, we recommend avoiding in-person civic activities. Instead, consider <a href="/get-involved-from-home" class="alert-link">these projects</a> that you can contribute to from home.
            </div>
          </v-col>
          <v-col md="2" sm="12" cols="12">
            <v-btn class="d-flex get-involved-btn" href="/get-involved-from-home">
              View Projects
            </v-btn>
          </v-col>
        </v-row>
    </v-alert>
</template>

<script>
export default {
    computed: {
        shouldDisplay: function () {
            return this.$nuxt.$route.path != '/get-involved-from-home';
        }
    }
}
</script>

<style scoped>
  .covid-alert{
    color: #9E0000 !important;
    background-color: #ffe9eb;
    border-radius:0px;
  }

  .covid-alert-text{
    font-size: 20px;
    margin-left:10px;
  }

  .covid-alert i {
    color: #9E0000;
  }

  .get-involved-btn{
    display:flex;
    margin-left:auto;
  }

  .get-involved-btn:hover{
    text-decoration: none;
  }

  .alert-link{
    color:#004A99;
    font-weight:normal;
  }
</style>