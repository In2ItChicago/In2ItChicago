<template>
	<div class="row justify-content-center">
		<div class="col-md-8 filters" v-if="$store.state.searchFilter">
			<div class="filter-row form-row justify-content-center">
				<div class="col-md-3">
					<label for="locationFilter" class="filter-label">Zip / Address</label>
					<input type="text" class="form-control" id="locationFilter" placeholder="Zip / Address" v-model="filterForm.address">
				</div>
				<div class="col-md-auto">
					<client-only placeholder="Loading...">
						<label for="startDatePicker" class="filter-label">From</label>
						<datepicker
							id="startDatePicker"
							v-model="filterForm.startTime"
							name="fromDatePicker"
							wrapper-class="datepicker"
							class="datepicker">
						</datepicker>
					</client-only>
				</div>
				<div class="col-md-3">
					<client-only placeholder="Loading...">
						<label for="endDatePicker" class="filter-label">To</label>
						<datepicker
							id="endDatePicker"
							v-model="filterForm.endTime"
							name="toDatePicker"
							wrapper-class="datepicker"
							class="datepicker">
						</datepicker>
					</client-only>
				</div>
			</div>

			<div class="filter-row form-row justify-content-center">
				<div class="col-md-2">
					<select class="form-control" id="distanceFilter" v-model="filterForm.miles">
						<option value="1">1 Mile</option>
						<option value="2">2 Miles</option>
						<option value="3">3 Miles</option>
						<option value="5">5 Miles</option>
						<option value="10">10 Miles</option>
						<option value="15">15 Miles</option>
					</select>
				</div>
				<div class="col-md-2">
					<input type="text" class="form-control" id="organization" placeholder="Organization" v-model="filterForm.organization">
				</div>
				<div class="col-md-2">
					<input type="text" class="form-control" id="neighborhood" placeholder="Neighborhood" v-model="filterForm.neighborhood">
				</div>
			</div>

			<div class="filter-row form-row justify-content-center">
				<div class="col-md-2">
					<button class="search-btn" @click="filter()">SEARCH</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
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
					organization: this.$store.state.searchFilter.organization,
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
			}
		}
	};
</script>