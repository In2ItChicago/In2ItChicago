<template>
	<div class="filters">
		<button class="accordion-button" @click="open">Filter Results</button>						
		<div class="accordion-panel">
			<div class="form-group">
				<label for="locationFilter">Where</label>
				<input type="text" class="form-control" id="locationFilter" placeholder="Zip / Neighborhood" :value="searchFilters.zipOrNeighborhood">
			</div>

			<div class="form-group">
				<label for="locationFilter">Distance (Miles)</label>
				<select class="form-control" id="distanceFilter" v-model="searchFilters.searchRadius">
					<option value="5">5</option>
					<option value="10">10</option>
					<option value="25">25</option>
					<option value="50">50</option>
					<option value="100">100</option>
				</select>
			</div>

			<div class="form-group">
				<label for="fromDatePicker">From</label>
				<datepicker :value="searchFilters.startDate" name="fromDatePicker" wrapper-class="datepicker" class="datepicker"></datepicker>
			</div>

			<div class="form-group">
				<label for="toDatePicker">To</label>
				<datepicker :value="searchFilters.endDate" name="toDatePicker" wrapper-class="datepicker" class="datepicker"></datepicker>
			</div>

			<div class="form-group text-right">
				<button class="btn btn-light" @click="$emit('filterApplied')">Filter</button>
			</div>
		</div>
			
		<button class="accordion-button" @click="open">Category</button>
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
		</div>
			
		<button class="accordion-button" @click="open">Advanced Options</button>
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
		</div>
	</div>
</template>

<script>
	import Datepicker from 'vuejs-datepicker';
	export default{
		props: ['searchFilters'],
		methods: {
			open: function(event) {
				event.target.classList.toggle('active');
				let panel = event.target.nextElementSibling;
				panel.classList.toggle('open');
				if (panel.style.maxHeight) {
					panel.style.maxHeight = null;
				}
				else {
					panel.style.maxHeight = panel.scrollHeight + 'px';
				} 
			}
		},
		components:{
			Datepicker
		}
	};
</script>