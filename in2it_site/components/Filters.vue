<template>
	<div class="filters">
		<div class="form-row filters-form-row">
			<div class="col-sm-2"></div>
			<div class="col-sm-2">
				<label for="locationFilter" class="filter-label">Where</label>
				<input type="text" class="form-control" id="locationFilter" placeholder="Zip / Neighborhood" v-model="searchFilter.addressOrZip">
			</div>
			<div class="col-sm-3">
				<label for="fromDatePicker" class="filter-label">From</label>
				<no-ssr placeholder="Loading...">
				<datepicker
					id="startDatePicker"
					v-model="searchFilter.startDate"
					name="fromDatePicker"
					wrapper-class="datepicker"
					class="datepicker">
				</datepicker>
				</no-ssr>
			</div>
			<div class="col-sm-3">
				<label for="toDatePicker" class="filter-label">To</label>
				<no-ssr placeholder="Loading...">
				<datepicker
					id="endDatePicker"
					v-model="searchFilter.endDate"
					name="toDatePicker"
					wrapper-class="datepicker"
					class="datepicker">
				</datepicker>
				</no-ssr>
			</div>
			<div class="col-sm-2"></div>
		</div>

		<div class="form-row filters-form-row">
			<div class="col-sm-3"></div>
			<div class="col-sm-2">
				<label for="locationFilter" class="filter-label">Distance (Miles)</label>
				<select class="form-control" id="distanceFilter" v-model="searchFilter.searchRadius">
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
					<option value="5">5</option>
					<option value="10">10</option>
					<option value="15">15</option>
				</select>
			</div>
			<div class="col-sm-2">
				<label for="organization" class="filter-label">Organization</label>
				<input type="text" class="form-control" id="organization" placeholder="Name" v-model="searchFilter.organization">
			</div>
			<div class="col-sm-2">
				<label for="organization" class="filter-label">Neighborhood</label>
				<input type="text" class="form-control" id="neighborhood" placeholder="Name" v-model="searchFilter.neighborhood">
			</div>
			<div class="col-sm-3"></div>
		</div>

		<div class="form-row filters-form-row">
			<div class="col-sm-5"></div>
			<div class="col-sm-2">
				<button class="btn btn-secondary btn-lg filter-btn" @click="filter()">Search</button>
			</div>
			<div class="col-sm-5"></div>
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
	let defaultFromDate = function() {
		return new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate());
	};
	let defaultToDate = function() {
		return new Date(new Date().getFullYear(), new Date().getMonth(),  new Date().getDate() + 7);
	};
	
	export default {
		data() {
			return {
				searchFilter: {
					addressOrZip: '60647',
					searchRadius: 3,
					organization: '',
					neighborhood: '',
					startDate: defaultFromDate(),
					endDate: defaultToDate(),
				}
			};
		},
		methods: {
			filter: function() {
				this.$store.searchFilter = this.searchFilter;
				this.$emit('filterApplied');
			}
		}
	};
</script>