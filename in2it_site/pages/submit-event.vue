<template>
    <div class="container">
        <div class="content-col col-md-8 offset-md-2 col-sm-12">
            <h1>Post an Event</h1>

            <v-form
                ref="form"
                lazy-validation
            >
                <v-row>
                    <h2>General Info</h2>
                </v-row>
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
                    <v-textarea
                        v-model="event.description"
                        label="Description of Event"
                        required
                    ></v-textarea>
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
                    <h2>Location</h2>
                </v-row>
                <v-row>
                    <v-checkbox
                        v-model="event.isHiddenFromPublic"
                        label="I don't want this event's location to be shown publicly"
                    ></v-checkbox>
                </v-row>
                <v-row v-if="!event.isHiddenFromPublic">
                    <v-text-field
                        v-model="event.addressLine1"
                        label="Event Address Line 1 (Optional)"
                    ></v-text-field>
                </v-row>
                <v-row v-if="!event.isHiddenFromPublic">
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
                    <h2>Date & Time</h2>
                </v-row>
                <v-row>
                    <v-col>
                        <v-label>Date of Event</v-label>
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
                                label="Event Start Date"
                                prepend-icon="mdi-calendar"
                                readonly
                                v-on="on"
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
                                label="Event End Date"
                                prepend-icon="mdi-calendar"
                                readonly
                                v-on="on"
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
                        <v-label>Start Time</v-label>
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
                            label="Hour"
                        ></v-select>
                        <v-select
                            :items="minuteSelectionItems"
                            v-model="event.startTimeMins"
                            label="Min"
                        ></v-select>
                        <v-select
                            :items="amPmSelectionItems"
                            v-model="event.startTimeAmPm"
                        ></v-select>
                    </v-col>
                    
                    <v-col class="d-flex flex-row">
                        <v-select
                            :items="hourSelectionItems"
                            v-model="event.endTimeHrs"
                            label="Hour"
                        ></v-select>
                        <v-select
                            :items="minuteSelectionItems"
                            v-model="event.endTimeMins"
                            label="Min"
                        ></v-select>
                        <v-select
                            :items="amPmSelectionItems"
                            v-model="event.endTimeAmPm"
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
                        <v-col class="d-flex flex-row">
                            <v-label>This is event is held</v-label>
                            <v-select :items="recurringTimeIntervals" v-model="event.recurringTimeInterval"></v-select>
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
                                    color="deep-purple accent-3"
                                    group
                                    multiple
                                >
                                    <v-btn value="Sunday">
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
                    <h2>Accessibility</h2>
                </v-row>
                <v-row>
                    <v-col>
                        <v-radio-group v-model="event.isHandicapAccessible" label="Is this event handicap accessible?" row>
                            <v-radio label="Yes" value="1"></v-radio>
                            <v-radio label="No" value="0"></v-radio>
                        </v-radio-group>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-radio-group v-model="event.requiresPhysicalActivities" label="Will participants be required to perform any strenuous physical activities?" row>
                            <v-radio label="Yes" value="1"></v-radio>
                            <v-radio label="No" value="0"></v-radio>
                        </v-radio-group>
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
                    endTimeHrs: '',
                    endTimeMins: '',
                    endTimeAmPm: '',
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
                return 'The ' + this.getOrdinalSuffix(this.event.startDate.getDate() + 1) + ' of every month';
            },
            recurringDayNumValue: function () {
                return this.getOrdinalSuffix(this.event.startDate.getDate() + 1)
            },
            recurringNthDayLabel: function () {
                return this.recurringNthDayValue + ' of every month';
            },
            recurringNthDayValue: function () {
                let nth = 1;
                let eventDayNum = (this.event.startDate.getDate() + 1);
                let eventMonth = this.event.startDate.getMonth();
                
                let eventDayName = this.getDayName(this.event.startDate);
                for (let i = 1; i < eventDayNum; ++i) {
                    let testDate = new Date(this.event.startDate.getYear() + '-' + (eventMonth + 1) + '-01');
                    
                    testDate.setDate(testDate.getDate() + i);
                    
                    if (testDate.getMonth() != eventMonth) break; //Reached end of month
                    if (this.getDayName(testDate) == eventDayName) {
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
            setStartDate: function (date) {
                this.event.startDate = new Date(date);
                this.event.weeklyRecurringDays.push(this.getDayName(this.event.startDate));
                this.event.startDatePickerValue = date;
            },
            setEndDate: function (date) {
                this.event.endDate = new Date(date);
                this.event.endDatePickerValue = date;
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
            getDayName: function (date) {
                //Adjusts weekday num to start at 1
                let adjustedDate = new Date(date);
                adjustedDate.setDate(adjustedDate.getDate() + 1);
                return adjustedDate.toLocaleDateString('en-US', { weekday: 'long' });
            }
        }
    };
</script>