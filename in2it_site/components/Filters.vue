<template>
	<div class="row justify-content-center">
		<div class="col-md-8 filters" v-if="$store.state.searchFilter">
			<div class="filter-row form-row justify-content-center">
				<div class="col-md-3">
					<label for="locationFilter" class="filter-label">Zip / Neighborhood</label>
					<input type="text" class="form-control" id="locationFilter" placeholder="Zip / Neighborhood" v-model="filterForm.address">
				</div>
				<div class="col-md-auto">
					<no-ssr placeholder="Loading...">
						<label for="startDatePicker" class="filter-label">From</label>
						<datepicker
							id="startDatePicker"
							v-model="filterForm.startTime"
							name="fromDatePicker"
							wrapper-class="datepicker"
							class="datepicker">
						</datepicker>
					</no-ssr>
				</div>
				<div class="col-md-3">
					<no-ssr placeholder="Loading...">
						<label for="endDatePicker" class="filter-label">To</label>
						<datepicker
							id="endDatePicker"
							v-model="filterForm.endTime"
							name="toDatePicker"
							wrapper-class="datepicker"
							class="datepicker">
						</datepicker>
					</no-ssr>
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
			
<!-- Disabled until event categorization is improved
	
	<div class="accordion-panel">
		<div class="form-group">
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="libraryCheck">
				<label class="form-check-label" for="libraryCheck">
					Library
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="educationCheck">
				<label class="form-check-label" for="educationCheck">
					Education
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="environmentCheck" disabled>
				<label class="form-check-label" for="environmentCheck">
					Environment
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="homelessnessCheck" disabled>
				<label class="form-check-label" for="homelessnessCheck">
					Homelessness
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="hospitalsCheck" disabled>
				<label class="form-check-label" for="hospitalsCheck">
					Hospitals
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="hungerCheck" disabled>
				<label class="form-check-label" for="hungerCheck">
					Hunger
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="elderlyCheck" disabled>
				<label class="form-check-label" for="elderlyCheck">
					Elderly
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="kidsCheck" disabled>
				<label class="form-check-label" for="kidsCheck">
					Kids
				</label>
			</div>
		</div>
	</div> -->
			
	<!--
	<div class="accordion-panel">
		<div class="form-group">
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="closeToCTACheck">
				<label class="form-check-label" for="closeToCTACheck">
					Close to CTA
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="freeCheck">
				<label class="form-check-label" for="freeCheck">
					Free
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="noRSVPCheck">
				<label class="form-check-label" for="noRSVPCheck">
					No RSVP
				</label>
			</div>
			<div class="form-check">
				<input class="form-check-input" type="checkbox" value="" id="reoccurringCheck">
				<label class="form-check-label" for="reoccurringCheck">
					Reoccurring Events
				</label>
			</div>
		</div>
	</div> -->


<script>
	export default {
		data() {
			return {
				filterForm: {
					startTime: this.$store.state.searchFilter.startTime,
					endTime: this.$store.state.searchFilter.endTime,
					miles: this.$store.state.searchFilter.miles,
					address: this.$store.state.searchFilter.address,
					organization: this.$store.state.searchFilter.organization,
					neighborhood: this.$store.state.searchFilter.neighborhood
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