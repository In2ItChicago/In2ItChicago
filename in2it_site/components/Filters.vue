<template>
	<div class="row justify-content-center">
		<div class="col-md-8 filters" v-if="$store.state.searchFilter">
			<div class="filter-row form-row justify-content-center">
				<div class="col-md-4 col-sm-12">
					<client-only>
						<label for="locationFilter" class="filter-label">Zip / Address</label>
						<input type="text" class="form-control" id="locationFilter" placeholder="Zip / Address (Optional)" v-model="filterForm.address">
					</client-only>
				</div>
				<div class="col-md-auto col-sm-12 datepicker-group">
					<client-only>
						<div class="datepicker-input">
							<label for="startDatePicker" class="filter-label">From</label>
							<datepicker
								id="startDatePicker"
								v-model="filterForm.startTime"
								name="fromDatePicker"
								class="datepicker"
								input-class="datepicker-left">
							</datepicker>
						</div>
						
					
						<img src="/img/arrow.svg" class="date-arrow"/>

						<div class="datepicker-input">
							<label for="endDatePicker" class="filter-label">To</label>
							<datepicker
								id="endDatePicker"
								v-model="filterForm.endTime"
								name="toDatePicker"
								class="datepicker"
								input-class="datepicker-right">
							</datepicker>
						</div>
					</client-only>
				</div>
			</div>

			<div class="filter-row form-row justify-content-center">
				<client-only>
					<div class="col-sm-12 col-md-4 col-lg-3">
						<label for="keywords" class="d-md-none filter-label">Organization</label>
						<input type="text" class="form-control" id="keywords" placeholder="Keywords (Optional)" v-model="filterForm.keywords">
					</div>
					<div class="col-sm-12 col-md-4 col-lg-3">
						<label for="distanceFilter" class="d-md-none filter-label">Distance</label>
						<select class="form-control" id="distanceFilter" v-model="filterForm.miles">
							<option value="1">1 Mile</option>
							<option value="2">2 Miles</option>
							<option value="3">3 Miles</option>
							<option value="5">5 Miles</option>
							<option value="10">10 Miles</option>
							<option value="15">15 Miles</option>
						</select>
					</div>
					<div class="col-sm-12 col-md-4 col-lg-3">
						<neighborhood-autocomplete @changed="setNeighborhood"></neighborhood-autocomplete>
					</div>
				</client-only>
			</div>

			<div class="filter-row form-row justify-content-center">
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
				filterForm: {
					startTime: this.$store.state.searchFilter.startTime,
					endTime: this.$store.state.searchFilter.endTime,
					miles: this.$store.state.searchFilter.miles,
					address: this.$store.state.searchFilter.address,
					keywords: this.$store.state.searchFilter.keywords,
					neighborhood: this.$store.state.searchFilter.neighborhood,
					limit: this.$store.state.searchFilter.limit
				}
			};
		},
		methods: {
			setEndTime: function() {
				// Manually set the time to 11:59 PM for now because we don't have a time picker yet
				this.filterForm.endTime.setHours(23, 59, 59);
			},
			filter: function() {
				this.setEndTime();
				this.$store.commit('searchFilter/set', this.filterForm);
				this.$emit('filterApplied');
			},
			setNeighborhood: function(neighborhood) {
				this.filterForm.neighborhood = neighborhood;
			}
		},
		components: {
			NeighborhoodAutocomplete
		}
	};
</script>

<style scoped>
	@media (max-width: 768px) {
        .filter-row{
            margin-top:0px;
		}
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
		.datepicker-input{
			width:46vw;
		}
		.date-arrow{
			width:8vw;
		}
    }
</style>