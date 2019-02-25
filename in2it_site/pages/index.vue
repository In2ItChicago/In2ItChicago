<template>
	<div>
		<div class="content">
			<filters :searchFilters="searchFilters" @filterApplied="updateEvents()"></filters>
			<event-list :events="events"></event-list>
		</div>
	</div>	
</template>

<script lang='ts'>
	import axios from 'axios';
	import rest from '@feathersjs/rest-client';
	import feathers from '@feathersjs/feathers';
	import Filters from '~/components/Filters.vue';
	import EventList from '~/components/EventList.vue';
	
    import { dummyData } from '~/store/dummydata.js';

	const app = feathers();
	const restClient = rest('http://event_service:5000');
	app.configure(restClient.axios(axios));
    const events = app.service('events');

	export default {
		data() {
			return {
				events: [],
				searchFilters: {
					zipOrNeighborhood: '',
					searchRadius: 10,
					startDate: new Date(new Date().getFullYear(), new Date().getMonth() + 1,  new Date().getDate()),
					endDate: new Date(new Date().getFullYear(), new Date().getMonth() + 1,  new Date().getDate())
				}
			};
		},
		asyncData ({ params }) {
            //Ensure get request goes to an endpoint that returns an array or json object
            //If a regular HTML page is returned, the v-for in the view above will try to
            //render each character in the HTML page string as a separate event and nuxt
            //will run out of memory
            if (process.env.DUMMY_DATA) {
                return { events: dummyData };
            }
			return events.find({query: {start_timestamp: 0, end_timestamp: 10000000000000}})
				.then(res => {
					return { events: res.data };
				});
		},
		methods:{
			updateEvents: function(){
				events.find({query: {
					start_timestamp: this.searchFilters.startDate,
					end_timestamp: this.searchFilters.endDate
				}})
				.then(res => {
					return { events: res.data };
				});

				/* This gives a CORS Error
				 return axios.get('http://localhost:5000/events?start_timestamp=0&end_timestamp=10000000000000')
				.then((res) => {
					return {events: res.data};
				}); */
			}
		},
		components: {
			Filters,
			EventList
		}
	};
</script>
