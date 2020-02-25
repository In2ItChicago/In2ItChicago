<template>
    <div class="container">
        <div class="content-col col-md-8 offset-md-2 col-sm-12">
            <v-row class="page-heading-row">
                <v-col>
                    <h1 class="post-event-heading">Post an Event</h1>
                </v-col>
            </v-row>

            <v-form
                ref="form"
                lazy-validation
            >
                <v-row>
                    <v-col sm="12" md="8">
                        <v-row>
                            <h2 class="post-event-subheading">General Info</h2>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-label>
                                    Organization
                                    <span class="required-star"> *</span>
                                </v-label>
                                <v-text-field
                                    v-model="event.organization"
                                    required
                                    outlined
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-label>
                                    Event Title
                                    <span class="required-star"> *</span>
                                </v-label>
                                <v-text-field
                                    v-model="event.title"
                                    required
                                    outlined
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-label>
                                    Description of Event
                                    <span class="required-star"> *</span>
                                </v-label>
                                <v-textarea
                                    v-model="event.description"
                                    required
                                    outlined
                                ></v-textarea>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-label>
                                    Event URL (Optional)
                                </v-label>
                                <v-text-field
                                    v-model="event.url"
                                    hint="Link to a specific event is preferred, but link to a page containing general event listings is okay"
                                    outlined
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-label>
                                    Cost (Optional)
                                </v-label>
                                <v-text-field
                                    v-model="event.cost"
                                    prepend-inner-icon="mdi-currency-usd"
                                    outlined
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <h2 class="post-event-subheading">Location</h2>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-checkbox
                                    v-model="event.isHiddenFromPublic"
                                    label="I don't want this event's location to be shown publicly"
                                ></v-checkbox>
                            </v-col>
                        </v-row>
                        <v-row v-if="!event.isHiddenFromPublic">
                            <v-col>
                                <v-label>
                                    Event Address Line 1
                                    <span class="required-star"> *</span>
                                </v-label>
                                <v-text-field
                                    v-model="event.addressLine1"
                                    outlined
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row v-if="!event.isHiddenFromPublic">
                            <v-col>
                                <v-label>Event Address Line 2 (Optional)</v-label>
                                <v-text-field
                                    v-model="event.addressLine2"
                                    outlined
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-label>Neighborhood (Optional)</v-label>
                                <v-text-field
                                    v-model="event.neighborhood"
                                    hint="Input the Chicago neighborhood this event will be taking place in (i.e. Logan Square, Wrigleyville, etc.)"
                                    outlined
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <h2 class="post-event-subheading">Date & Time</h2>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-label>
                                    Event Start Date
                                    <span class="required-star"> *</span>
                                </v-label>
                                <v-menu
                                    ref="startDateMenu"
                                    v-model="isStartDatePickerOpen"
                                    :close-on-content-click="false"
                                    :return-value.sync="event.startDatePickerValue"
                                    transition="scale-transition"
                                    offset-y
                                    min-width="290px"
                                >
                                    <template v-slot:activator="{ on }">
                                        <v-text-field
                                            v-model="event.startDatePickerValue"
                                            prepend-inner-icon="mdi-calendar"
                                            readonly
                                            v-on="on"
                                            outlined
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker v-model="event.startDatePickerValue" no-title scrollable @change="setStartDate">
                                        <v-spacer></v-spacer>
                                        <v-btn text color="primary" @click="isStartDatePickerOpen = false">Cancel</v-btn>
                                        <v-btn text color="primary" @click="$refs.startDateMenu.save(event.startDatePickerValue)">OK</v-btn>
                                    </v-date-picker>
                                </v-menu>
                            </v-col>
                            <v-col v-if="event.isMultiDayEvent">
                                <v-label>Event End Date</v-label>
                                <v-menu
                                    ref="endDateMenu"
                                    v-model="isEndDatePickerOpen"
                                    :close-on-content-click="false"
                                    :return-value.sync="event.endDatePickerValue"
                                    transition="scale-transition"
                                    offset-y
                                    min-width="290px"
                                >
                                    <template v-slot:activator="{ on }">
                                        <v-text-field
                                            v-model="event.endDatePickerValue"
                                            prepend-inner-icon="mdi-calendar"
                                            readonly
                                            v-on="on"
                                            outlined
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker v-model="event.endDatePickerValue" no-title scrollable @change="setEndDate">
                                        <v-spacer></v-spacer>
                                        <v-btn text color="primary" @click="isEndDatePickerOpen = false">Cancel</v-btn>
                                        <v-btn text color="primary" @click="$refs.endDateMenu.save(event.endDatePickerValue)">OK</v-btn>
                                    </v-date-picker>
                                </v-menu>
                            </v-col>
                            <v-col>
                                <v-checkbox
                                    v-model="event.isMultiDayEvent"
                                    label="This is a multi day event"
                                ></v-checkbox>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-label>
                                    Start Time
                                    <span class="required-star"> *</span>
                                </v-label>
                            </v-col>
                            <v-col>
                                <v-label>End Time (Optional)</v-label>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col class="d-flex flex-row">
                                <v-select
                                    :items="hourSelectionItems"
                                    v-model="event.startTimeHrs"
                                    outlined
                                ></v-select>
                                <v-select
                                    :items="minuteSelectionItems"
                                    v-model="event.startTimeMins"
                                    outlined
                                ></v-select>
                                <v-select
                                    :items="amPmSelectionItems"
                                    v-model="event.startTimeAmPm"
                                    outlined
                                ></v-select>
                            </v-col>
                            
                            <v-col class="d-flex flex-row">
                                <v-select
                                    :items="hourSelectionItems"
                                    v-model="event.endTimeHrs"
                                    outlined
                                ></v-select>
                                <v-select
                                    :items="minuteSelectionItems"
                                    v-model="event.endTimeMins"
                                    outlined
                                ></v-select>
                                <v-select
                                    :items="amPmSelectionItems"
                                    v-model="event.endTimeAmPm"
                                    outlined
                                ></v-select>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-checkbox
                                v-model="event.isRecurring"
                                label="This is a recurring event"
                            ></v-checkbox>
                        </v-row>
                        <div v-if="event.isRecurring">
                            <v-row>
                                <v-col>
                                    <v-label>This is event is held</v-label>
                                    <v-select :items="recurringTimeIntervals" v-model="event.recurringTimeInterval" outlined></v-select>
                                </v-col>
                            </v-row>
                            <v-row v-if="event.recurringTimeInterval == 'Weekly'">
                                <v-col>
                                    <v-row>
                                        <v-label v-if="event.weeklyRecurringDays.length">
                                            {{ weeklyRecurringDaysLabelText }}
                                        </v-label>
                                    </v-row>
                                    <v-row>
                                        <v-btn-toggle
                                            v-model="event.weeklyRecurringDays"
                                            tile
                                            background-color="primary"
                                            group
                                            multiple
                                        >
                                            <v-btn value="Sunday" class="weekday-button">
                                                Su
                                            </v-btn>

                                            <v-btn value="Monday">
                                                M
                                            </v-btn>

                                            <v-btn value="Tuesday">
                                                Tu
                                            </v-btn>

                                            <v-btn value="Wednesday">
                                                W
                                            </v-btn>

                                            <v-btn value="Thursday">
                                                Th
                                            </v-btn>

                                            <v-btn value="Friday">
                                                F
                                            </v-btn>

                                            <v-btn value="Saturday">
                                                Sa
                                            </v-btn>
                                        </v-btn-toggle>
                                    </v-row>
                                </v-col>
                            </v-row>
                            <v-row v-if="event.recurringTimeInterval == 'Monthly'">
                                <v-col>
                                    <v-radio-group v-model="event.monthlyRecurringValue">
                                        <v-radio :label="recurringDayNumLabel" :value="recurringDayNumValue"></v-radio>
                                        <v-radio :label="recurringNthDayLabel" :value="recurringNthDayValue"></v-radio>
                                    </v-radio-group>
                                </v-col>
                            </v-row>
                        </div>
                        <v-row>
                            <h2 class="post-event-subheading">Accessibility</h2>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-label>
                                    Is this event handicap accessible?
                                    <span class="required-star"> *</span>
                                </v-label>
                                <v-radio-group v-model="event.isHandicapAccessible" row>
                                    <v-radio label="Yes" value="1"></v-radio>
                                    <v-radio label="No" value="0"></v-radio>
                                </v-radio-group>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col>
                                <v-label>
                                    Will participants be required to perform any strenuous physical activities?
                                    <span class="required-star"> *</span>
                                </v-label>
                                <v-radio-group v-model="event.requiresPhysicalActivities" row>
                                    <v-radio label="Yes" value="1"></v-radio>
                                    <v-radio label="No" value="0"></v-radio>
                                </v-radio-group>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col>
                                <v-btn color="#173450" @click="submitEvent" dark large>Submit</v-btn>
                            </v-col>
                        </v-row>
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
                recurringTimeIntervals: ['Weekly', 'Monthly'],
                hourSelectionItems: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                minuteSelectionItems: [0, 15, 30, 45],
                amPmSelectionItems: ['AM', 'PM'],
				event: {
                    organization: '',
                    title: '',
                    description: '',
                    addressLine1: '',
                    addressLine2: '',
                    neighborhood: '',
                    url: '',
                    cost: '',
                    isHiddenFromPublic: false,
                    isMultiDayEvent: false,
                    startDate: new Date(),
                    endDate: new Date(),
                    startDatePickerValue: '',
                    endDatePickerValue: '',
                    startTimeHrs: 9,
                    startTimeMins: 0,
                    startTimeAmPm: 'AM',
                    endTimeHrs: 12,
                    endTimeMins: 0,
                    endTimeAmPm: 'PM',
                    isRecurring: false,
                    recurringTimeInterval: 'Weekly',
                    weeklyRecurringDays: [],
                    monthlyRecurringValue: '',
                    isHandicapAccessible: false,
                    requiresPhysicalActivities: false
                }
			};
        },
        computed: {
            recurringDayNumLabel: function () {
                return 'The ' + this.getOrdinalSuffix(this.event.startDate.getDate()) + ' of every month';
            },
            recurringDayNumValue: function () {
                return this.getOrdinalSuffix(this.event.startDate.getDate());
            },
            recurringNthDayLabel: function () {
                return this.recurringNthDayValue + ' of every month';
            },
            recurringNthDayValue: function () {
                let nth = 0;
                let eventDayNum = this.event.startDate.getDate();
                let eventMonth = this.event.startDate.getMonth();
                let eventDayName = this.getDayName(this.event.startDate);

                for (let i = 0; i < eventDayNum; ++i) {
                    //Start at first date of current month
                    let testDateString = this.event.startDate.getFullYear() + '-' + (eventMonth + 1) + '-1';
                    let testDate = this.getDateObjectFromYYYYMMDD(testDateString);

                    //Iterate through days of month
                    testDate.setDate(testDate.getDate() + i);

                    if (testDate.getMonth() != eventMonth) break; //Reached end of month
                    if (this.getDayName(testDate) == eventDayName) { //Day name matches
                        ++nth;
                    }
                }
                return this.getOrdinalSuffix(nth) + ' ' + this.getDayName(this.event.startDate);
            },
            weeklyRecurringDaysLabelText: function () {
                if (this.event.weeklyRecurringDays.length <= 0) {
                    return '';
                }
                else if (this.event.weeklyRecurringDays.length == 1) {
                    return 'Every ' + this.event.weeklyRecurringDays[0];
                }
                else if (this.event.weeklyRecurringDays.length == 2) {
                    return 'Every ' + this.event.weeklyRecurringDays[0] + ' and ' + this.event.weeklyRecurringDays[1];
                }
                else {
                    let text = 'Every ';
                    for (let i in this.event.weeklyRecurringDays) {
                        if (i < this.event.weeklyRecurringDays.length - 1) {
                            text += this.event.weeklyRecurringDays[i] + ', ';
                        }
                        else { //Use 'and' instead of comma on last day
                            text += 'and ' + this.event.weeklyRecurringDays[i];
                        }
                    }
                    return text;
                }
            }
        },
        methods: {
            getDateObjectFromYYYYMMDD: function (YYYYMMDD) {
                let datePieces = YYYYMMDD.split('-');
                return new Date(datePieces[0], (datePieces[1] - 1), datePieces[2]);
            },
            setStartDate: function (YYYYMMDD) {
                this.event.startDate = this.getDateObjectFromYYYYMMDD(YYYYMMDD);
                this.event.weeklyRecurringDays = [this.getDayName(this.event.startDate)];
                this.event.startDatePickerValue = YYYYMMDD;
            },
            setEndDate: function (YYYYMMDD) {
                this.event.endDate = this.getDateObjectFromYYYYMMDD(YYYYMMDD);
                this.event.endDatePickerValue = YYYYMMDD;
            },
            submitEvent: function () {
                console.log('submitEvent called');
                console.log(this.event);
            },
            getOrdinalSuffix: function (i) {
                let j = i % 10,
                    k = i % 100;
                if (j == 1 && k != 11) {
                    return i + "st";
                }
                if (j == 2 && k != 12) {
                    return i + "nd";
                }
                if (j == 3 && k != 13) {
                    return i + "rd";
                }
                return i + "th";
            },
            getDayName: function (dateObject) {
                return dateObject.toLocaleDateString('en-US', { weekday: 'long' });
            }
        }
    };
</script>

<style scoped>
    .page-heading-row {
        background-color: #173450;
    }

    .post-event-heading {
        color: #fff;
        font-size: 48px;
        margin-bottom: 0px;
    }

    .post-event-subheading {
        margin-top: 20px;
        font-weight: bold;
        font-size: 26px;
        color: rgba(0, 0, 0, 0.7);
    }

    .v-label {
        font-size: 16px;
        font-weight: bold;
        color: rgba(0, 0, 0, 0.6);
    }

    .v-input {
        border-radius: 0px;
    }

    .required-star {
        color: #c51313;
    }

    .weekday-button{
        border: 1px solid;
        border-color: #000;
    }
</style>