<template>
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
</template>

<script>
	import axios from 'axios';

	export default {
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