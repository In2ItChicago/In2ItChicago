<template>
    <div class="container">
        <div class="content-col col-md-8 offset-md-2 col-sm-12">
            <v-row class="page-heading-row">
                <v-col>
                    <h1 class="newcomers-heading">Newcomers</h1>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <ul>
                        <li>
                            <h2 class="newcomers-subheading">Want to keep in touch with the group?</h2>
                            <a class="newcomers-link" href="https://chihacknight.slack.com/archives/CT0JL33PG" target="_blank">
                                Join our Slack Channel
                            </a>
                        </li>
                        <li>
                            <h2 class="newcomers-subheading">Want to learn more about our project?</h2>
                            <a class="newcomers-link" href="https://docs.google.com/document/d/1DN8eAg0b5_NnD-9uPacn4FuPElMRbHbqOVqV7clTP3c/edit#heading=h.wn6boqyakn62" target="_blank">
                                Here is our welcome wagon document
                            </a>
                        </li>
                        <li>
                            <h2 class="newcomers-subheading">Want to see which sites we're writing scrapers for?</h2>
                            <a class="newcomers-link" href="https://docs.google.com/spreadsheets/d/1EgsQDy2nQQxqfBi9M9kAPOrnU-LCjVcmF3-8mZohDj4/edit#gid=0" target="_blank">
                                Here is the spreadsheet
                            </a>
                        </li>
                        <li>
                            <h2 class="newcomers-subheading">Want to contribute to development?</h2>
                            <a class="newcomers-link" href="https://github.com/In2ItChicago/In2ItChicago" target="_blank">
                                Here is our Github Repository
                            </a>
                        </li>
                    </ul>
                </v-col>
            </v-row>
        </div>
    </div>
</template>

<style scoped>
    .page-heading-row {
        background-color: #173450;
    }

    .newcomers-heading {
        color: #fff;
        font-size: 48px;
        margin-bottom: 0px;
    }

    .newcomers-subheading {
        margin-top: 20px;
        font-weight: bold;
        font-size: 26px;
        color: rgba(0, 0, 0, 0.7);
    }
</style>