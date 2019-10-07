<template>
	<div class="row justify-content-center">
		<div class="col-md-8 filters" v-if="$store.state.searchFilter">
			<div class="filter-row form-row justify-content-center">
				<div class="col-md-3">
					<label for="locationFilter" class="filter-label">Zip / Address</label>
					<input type="text" class="form-control" id="locationFilter" placeholder="Zip / Address" v-model="filterForm.address">
				</div>
				<div class="col-md-auto datepicker-group">
					<div class="datepicker-input">
						<client-only placeholder="Loading...">
							<label for="startDatePicker" class="filter-label">From</label>
							<datepicker
								id="startDatePicker"
								v-model="filterForm.startTime"
								name="fromDatePicker"
								class="datepicker"
								input-class="datepicker-left">
							</datepicker>
						</client-only>
					</div>
					
					<img src="/img/arrow.svg" class="date-arrow"/>

					<div class="datepicker-input">
						<client-only placeholder="Loading...">
							<label for="endDatePicker" class="filter-label">To</label>
							<datepicker
								id="endDatePicker"
								v-model="filterForm.endTime"
								name="toDatePicker"
								class="datepicker"
								input-class="datepicker-right">
							</datepicker>
						</client-only>
					</div>
				</div>
			</div>

			<div class="filter-row form-row justify-content-center">
				<div class="col-md-2">
					<input type="text" class="form-control" id="organization" placeholder="Organization" v-model="filterForm.organization">
				</div>
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
					<div class="autocomplete">
						<input
							class="neighborhood-input form-control"
							id="neighborhood" 
							placeholder="Neighborhood" 
							v-model="autocompleteResult"
							@input="autocompleteNeighborhood"
							autocomplete="off">
						<ul v-show="autocompleteOpen" class="autocomplete-results">
							<li v-for="(result, i) in autocompleteResults" :key="i" class="autocomplete-result" @click="setResult(result)">
								{{ result }}
							</li>
						</ul>
					</div>
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
	import axios from 'axios';

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
				},
				neighborhoods: [],
				autocompleteOpen: false,
				autocompleteResults: [],
				autocompleteResult: ''
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
			autocompleteNeighborhood: function() {
				this.autocompleteOpen = true;
				this.filterResults();
			},
			filterResults: function() {
				this.autocompleteResults = this.neighborhoods.filter(item => item.toLowerCase().indexOf(this.autocompleteResult.toLowerCase()) > -1);
			},
			setResult: function(result) {
				this.autocompleteResult = result;
				this.autocompleteOpen = false;
				this.filterForm.neighborhood = result;
			}
		},
		computed: {
			neighborhoodsUrl: function() {
				const eventURL = process.server ? 'event_service:5000' : this.$env.IN2IT_API_URL;
				return `http://${eventURL}/geocode/listNeighborhoods`;
			}
		},
		mounted() {
			return axios.get(this.neighborhoodsUrl)
			.then((res) => {
				this.neighborhoods = res.data;
			});
		}
	};
</script>