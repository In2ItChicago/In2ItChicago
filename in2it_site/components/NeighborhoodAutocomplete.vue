<template>
    <div>
		<v-text-field 
			solo 
			hide-details
			v-model="autocompleteResult" 
			id="neighborhood" 
			placeholder="Neighborhood (Optional)" 
			background-color="#fff" 
			@input="autocompleteNeighborhood"
            autocomplete="off"
			:class="textfieldClass"
			:hint="hint">
		</v-text-field>	
        <ul v-show="autocompleteOpen" :class="autocompleteResultsClass">
            <li v-for="(result, i) in autocompleteResults" :key="i" class="autocomplete-result" @click="setResult(result)">
                {{ result }}
            </li>
        </ul>
    </div>
</template>

<script>
	import axios from 'axios';

	export default {
		props: ['textfieldClass', 'resultsClass', 'hint'],
		data() {
			return {
				neighborhoods: [],
				autocompleteOpen: false,
				autocompleteResults: [],
				autocompleteResult: ''
			};
		},
		methods: {
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
                this.$emit('changed', result);
			}
		},
		computed: {
			neighborhoodsUrl: function() {
				const eventURL = process.server ? 'http://event_service:5000' : this.$env.IN2IT_API_URL;
				return `${eventURL}/geocode/listNeighborhoods`;
			},
			autocompleteResultsClass: function () {
				return this.resultsClass + ' autocomplete-results';
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

<style scoped>
	@media (max-width: 768px) {
		.filter-label{
			margin-top:12px;
		}
    }
</style>