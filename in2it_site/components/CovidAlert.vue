<template>    
    <v-alert v-if="shouldDisplay" prominent class="covid-alert">
        <v-row align="center">
            <v-col class="d-flex flex-row">
                <v-icon>
                    mdi-alert-circle
                </v-icon>
                <div class="covid-alert-text">
                    To help in the fight against COVID-19, we recommend avoiding in-person civic activities. Instead, consider <a href="/get-involved-from-home">these projects</a> that you can contribute to from home.
                </div>
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