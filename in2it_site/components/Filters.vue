<template>
	<div class="filters">
		<button class="accordion-button active" @click="toggle">Filter Results</button>						
		<div class="accordion-panel open" style="max-height:600px">
			<div class="form-group">
				<label for="locationFilter">Where</label>
				<input type="text" class="form-control" id="locationFilter" placeholder="Zip / Neighborhood" v-model="searchFilter.addressOrZip">
			</div>

			<div class="form-group">
				<label for="locationFilter">Distance (Miles)</label>
				<select class="form-control" id="distanceFilter" v-model="searchFilter.searchRadius">
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
					<option value="5">5</option>
					<option value="10">10</option>
					<option value="15">15</option>
				</select>
			</div>

			<div class="form-group">
				<label for="fromDatePicker">From</label>
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

			<div class="form-group">
				<label for="toDatePicker">To</label>
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

			<div class="form-group">
				<label for="organization">Organization</label>
				<input type="text" class="form-control" id="organization" placeholder="Enter Organization name" v-model="searchFilter.organization">
			</div>

			<div class="form-group">
				<label for="organization">Neighborhood</label>
				<input type="text" class="form-control" id="neighborhood" placeholder="Enter Neighborhood name" v-model="searchFilter.neighborhood">
			</div>

			<div class="form-group text-right">
				<button class="btn btn-light" @click="filter()">Filter</button>
			</div>
		</div>
			
<!-- Disabled until event categorization is improved
	<button class="accordion-button" @click="toggle">Category</button>
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
			
		<!-- <button class="accordion-button" @click="toggle">Advanced Options</button>
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
	</div>
</template>

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
			toggle: function(event) {
				event.target.classList.toggle('active');
				let panel = event.target.nextElementSibling;
				panel.classList.toggle('open');
				if (panel.style.maxHeight) {
					panel.style.maxHeight = null;
				}
				else {
					panel.style.maxHeight = panel.scrollHeight + 'px';
				} 
			},
			filter: function() {
				this.$store.searchFilter = this.searchFilter;
				this.$emit('filterApplied');
			}
		}
	};
</script>