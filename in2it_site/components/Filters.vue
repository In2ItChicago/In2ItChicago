<template>
	<div class="row justify-content-center">
		<div class="col-md-8 filters" v-if="$store.state.searchFilter">
			<div class="form-row justify-content-center">
				<div class="col-md-4 col-sm-12">
					<client-only>
						<label for="locationFilter" class="filter-label">Zip / Address</label>
						<v-text-field 
							solo 
							height="56"
							v-model="filterForm.address" 
							id="locationFilter" 
							placeholder="Zip / Address (Optional)" 
							background-color="#fff">
						</v-text-field>
					</client-only>
				</div>
				<div class="col-md-auto col-sm-12 datepicker-group">
					<client-only>
						<div class="datepicker-input">
							<label class="filter-label">
								Event Start Date
							</label>
							<v-menu
								ref="startDateMenu"
								v-model="isStartDatePickerOpen"
								:close-on-content-click="false"
								:return-value.sync="filterForm.startDatePickerValue"
								transition="scale-transition"
								offset-y
								min-width="290px"
							>
								<template v-slot:activator="{ on }">
									<v-text-field
										v-model="filterForm.startDatePickerValue"
										prepend-inner-icon="mdi-calendar"
										readonly
										hide-details
										v-on="on"
										class="datepicker-text-field-left"
									></v-text-field>
								</template>
								<v-date-picker v-model="filterForm.startDatePickerValue" no-title scrollable @change="setStartDate" class="in2it-datepicker" color="#173450">
									<v-spacer></v-spacer>
									<v-btn text color="primary" @click="isStartDatePickerOpen = false">Cancel</v-btn>
									<v-btn text color="primary" @click="$refs.startDateMenu.save(filterForm.startDatePickerValue)">OK</v-btn>
								</v-date-picker>
							</v-menu>
						</div>
						
						<div class="datepicker-input">
							<label class="filter-label">
								Event End Date
							</label>
							<v-menu
								ref="endDateMenu"
								v-model="isEndDatePickerOpen"
								:close-on-content-click="false"
								:return-value.sync="filterForm.endDatePickerValue"
								transition="scale-transition"
								offset-y
								min-width="290px"
							>
								<template v-slot:activator="{ on }">
									<v-text-field
										v-model="filterForm.endDatePickerValue"
										prepend-inner-icon="mdi-calendar"
										readonly
										hide-details
										v-on="on"
										class="datepicker-text-field-right"
									></v-text-field>
								</template>
								<v-date-picker v-model="filterForm.endDatePickerValue" no-title scrollable @change="setEndDate" color="#173450">
									<v-spacer></v-spacer>
									<v-btn text color="primary" @click="isEndDatePickerOpen = false">Cancel</v-btn>
									<v-btn text color="primary" @click="$refs.endDateMenu.save(filterForm.endDatePickerValue)">OK</v-btn>
								</v-date-picker>
							</v-menu>
						</div>
					</client-only>
				</div>
			</div>

			<div class="form-row justify-content-center">
				<client-only>
					<div class="col-sm-12 col-md-4 col-lg-3">
						<label for="keywords" class="d-md-none filter-label">Keywords</label>			
						<v-text-field solo v-model="filterForm.keywords" id="keywords" placeholder="Keywords (Optional)" background-color="#fff">
						</v-text-field>
					</div>
					<div class="col-sm-12 col-md-4 col-lg-3">
						<label for="distanceFilter" class="d-md-none filter-label">Distance</label>
						<v-select
							:items="distances"
							id="distanceFilter" 
							v-model="filterForm.miles"
							solo
						></v-select>
					</div>
					<div class="col-sm-12 col-md-4 col-lg-3">
						<label for="neighborhood" class="d-md-none filter-label">Neighborhood</label>
						<neighborhood-autocomplete @changed="setNeighborhood"></neighborhood-autocomplete>
					</div>
				</client-only>
			</div>

			<div class="form-row justify-content-center">
				<div class="col-md-4 col-lg-2 col-sm-12">
					<client-only>
						<button class="search-btn" @click="filter()">SEARCH</button>
					</client-only>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import NeighborhoodAutocomplete from '~/components/NeighborhoodAutocomplete.vue';

   /** 
   * @vue-data {Number} startTime - the start time for the filter 
   * @vue-data {Number} endTime - the end time for the filter 
   * @vue-data {Number} miles - filter for how far away a location can be from the adress
   * @vue-data {Number} address - the address where the search will start from
   * @vue-data {Number} organization - the organization filter option
   * @vue-data {Number} neighborhood - the neighborhood being filtered
   * @vue-data {Number} limit - The limit to the number of results returned
   */

	export default {
		data() {
			return {
				isStartDatePickerOpen: false,
				isEndDatePickerOpen: false,
				filterForm: {
					startTime: this.$store.state.searchFilter.startTime,
					endTime: this.$store.state.searchFilter.endTime,
					startDatePickerValue: '',
					endDatePickerValue: '',
					miles: this.$store.state.searchFilter.miles,
					address: this.$store.state.searchFilter.address,
					keywords: this.$store.state.searchFilter.keywords,
					neighborhood: this.$store.state.searchFilter.neighborhood,
					limit: this.$store.state.searchFilter.limit
				},
				distances: [
					{text: '1 Mile', value: '1'},
					{text: '3 Miles', value: '3'},
					{text: '5 Miles', value: '5'},
					{text: '10 Miles', value: '10'},
					{text: '15 Miles', value: '15'}
				]
			};
		},
		methods: {
			getDateObjectFromYYYYMMDD: function (YYYYMMDD) {
                let datePieces = YYYYMMDD.split('-');
                return new Date(datePieces[0], (datePieces[1] - 1), datePieces[2]);
            },
			setStartDate: function (YYYYMMDD) {
                this.filterForm.startTime = this.getDateObjectFromYYYYMMDD(YYYYMMDD);
			},
			setEndDate: function (YYYYMMDD) {
				this.filterForm.endTime = this.getDateObjectFromYYYYMMDD(YYYYMMDD);
				// Manually set the time to 11:59 PM for now because we don't have a time picker yet
				this.filterForm.endTime.setHours(23, 59, 59);
			},
			filter: function() {
				this.$store.commit('searchFilter/set', this.filterForm);
				this.$emit('filterApplied');
			},
			setNeighborhood: function(neighborhood) {
				this.filterForm.neighborhood = neighborhood;
			}
		},
		mounted () {
			this.filterForm.startDatePickerValue = this.filterForm.startTime.getFullYear() + '-' + (this.filterForm.startTime.getMonth() + 1) + '-' + (this.filterForm.startTime.getDate() + 1);
			this.filterForm.endDatePickerValue = this.filterForm.endTime.getFullYear() + '-' + (this.filterForm.endTime.getMonth() + 1) + '-' + (this.filterForm.endTime.getDate() + 1);
		},
		components: {
			NeighborhoodAutocomplete
		}
	};
</script>

<style scoped>
	.datepicker-text-field-left.v-input {
		border-radius: 5px 0px 0px 5px;
		border:none;
		background-color:#fff;
		padding:12px;
		margin-top:0px;
	}

	.datepicker-text-field-right.v-input {
		border-radius: 0px 5px 5px 0px;
		border:none;
		background-color:#fff;
		padding:12px;
		margin-top:0px;
	}

	@media (max-width: 768px) {
		.filters{
			padding: 12px 28px 12px 28px;
			margin-top: 12px;
		}
		.filter-label{
			margin-top:12px;
		}
		.search-btn{
			margin-top:10px;
			margin-bottom:0px;
			width:100%;
		}
    }
</style>