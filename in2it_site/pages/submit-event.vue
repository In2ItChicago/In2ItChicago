<template>
    <div class="container">
        <div class="content-col col-md-8 offset-md-2 col-sm-12">
            <h1>Post an Event</h1>

            <v-form
                ref="form"
                lazy-validation
            >
                <v-row>
                    <v-text-field
                        v-model="event.organization"
                        label="Organization"
                        required
                    ></v-text-field>
                </v-row>
                <v-row>
                    <v-text-field
                        v-model="event.title"
                        label="Event Title"
                        required
                    ></v-text-field>
                </v-row>
                <v-row>
                    <v-text-field
                        v-model="event.description"
                        label="Description of Event"
                        required
                    ></v-text-field>
                </v-row>
                <v-row>
                    <v-text-field
                        v-model="event.addressLine1"
                        label="Event Address Line 1 (Optional)"
                    ></v-text-field>
                </v-row>
                <v-row>
                    <v-text-field
                        v-model="event.addressLine2"
                        label="Event Address Line 2 (Optional)"
                    ></v-text-field>
                </v-row>
                <v-row>
                    <v-text-field
                        v-model="event.neighborhood"
                        label="Neighborhood (Optional)"
                        hint="Input the Chicago neighborhood this event will be taking place in (i.e. Logan Square, Wrigleyville, etc.)"
                    ></v-text-field>
                </v-row>
                <v-row>
                    <v-text-field
                        v-model="event.url"
                        label="Event URL (Optional)"
                        hint="Link to a specific event is preferred, but link to a page containing general event listings is okay"
                    ></v-text-field>
                </v-row>
                <v-row>
                    <v-text-field
                        v-model="event.cost"
                        label="Cost (Optional)"
                        prepend-icon="mdi-currency-usd"
                    ></v-text-field>
                </v-row>
                <v-row>
                    <v-btn class="ma-2" outlined large color="indigo">
                        <v-icon>mdi-human-female-boy</v-icon>
                        <span class="hidden-sm-and-down">Family</span>
                    </v-btn>

                    <v-btn class="ma-2" outlined large color="indigo">
                        <v-icon>mdi-earth</v-icon>
                        <span class="hidden-sm-and-down">Cultural</span>
                    </v-btn>

                    <v-btn class="ma-2" outlined large color="indigo">
                        <v-icon>mdi-pine-tree</v-icon>
                        <span class="hidden-sm-and-down">Environmental</span>
                    </v-btn>
                </v-row>

                <v-row>
                    <v-col>
                        <v-menu
                            ref="startDateMenu"
                            v-model="isStartDatePickerOpen"
                            :close-on-content-click="false"
                            :return-value.sync="event.startDate"
                            transition="scale-transition"
                            offset-y
                            min-width="290px"
                        >
                            <template v-slot:activator="{ on }">
                                <v-text-field
                                v-model="event.startDate"
                                label="Event Start Date"
                                prepend-icon="mdi-calendar"
                                readonly
                                v-on="on"
                                ></v-text-field>
                            </template>
                            <v-date-picker v-model="event.startDate" no-title scrollable>
                                <v-spacer></v-spacer>
                                <v-btn text color="primary" @click="isStartDatePickerOpen = false">Cancel</v-btn>
                                <v-btn text color="primary" @click="$refs.startDateMenu.save(event.startDate)">OK</v-btn>
                            </v-date-picker>
                        </v-menu>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-menu
                            ref="endDateMenu"
                            v-model="isEndDatePickerOpen"
                            :close-on-content-click="false"
                            :return-value.sync="event.endDate"
                            transition="scale-transition"
                            offset-y
                            min-width="290px"
                        >
                            <template v-slot:activator="{ on }">
                                <v-text-field
                                v-model="event.endDate"
                                label="Event End Date"
                                prepend-icon="mdi-calendar"
                                readonly
                                v-on="on"
                                ></v-text-field>
                            </template>
                            <v-date-picker v-model="event.endDate" no-title scrollable>
                                <v-spacer></v-spacer>
                                <v-btn text color="primary" @click="isEndDatePickerOpen = false">Cancel</v-btn>
                                <v-btn text color="primary" @click="$refs.endDateMenu.save(event.endDate)">OK</v-btn>
                            </v-date-picker>
                        </v-menu>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-btn @click="submitEvent">Submit</v-btn>
                    </v-col>
                </v-row>
            </v-form>
        </div>
    </div>
</template>

<script>
    export default{
        data() {
			return {
                isStartDatePickerOpen: false,
                isEndDatePickerOpen: false,
				event: {
                    organization: '',
                    title: '',
                    description: '',
                    addressLine1: '',
                    addressLine2: '',
                    neighborhood: '',
                    url: '',
                    cost: '',

                    startDate: new Date().toISOString().substr(0, 10),
                    endDate: new Date().toISOString().substr(0, 10),
                }
			};
        },
        methods: {
            submitEvent: function () {
                console.log('submitEvent called');
                console.log(this.event);
            }
        }
    };
</script>