<template>
	<div>
		<header>
			<page-header></page-header>
		</header>
		<aside>
			<control-column></control-column>
		</aside>
		<main>
			<map-view></map-view>
			<event-results :events="events"></event-results>
		</main>
	</div>
</template>

<script>
	import axios from 'axios';
	import feathers from '@feathersjs/feathers';
	import rest from '@feathersjs/rest-client';
	import ControlColumn from '~/components/ControlColumn';
	import EventListing from '~/components/EventListing';
	import PageHeader from '~/components/PageHeader';
	import MapView from '~/components/MapView';
	import EventResults from '~/components/EventResults';

	const app = feathers();
	const restClient = rest('http://clipboard_db_client:5000');
	app.configure(restClient.axios(axios));
	const events = app.service('events');

	export default {
		data() {
			return {
				events: []
			};
		},
		asyncData ({ params }) {

            //Ensure get request goes to an endpoint that returns an array or json object
            //If a regular HTML page is returned, the v-for in the view above will try to
            //render each character in the HTML page string as a separate event and nuxt
            //will run out of memory

            /*return axios.get('http://localhost/')
                .then((res) => {
                    return { events: res.data }
				})*/
			return events.find({start_timestamp: 0, end_timestamp: 10000000000000});

			//Hardcoded test data until JSON api is linked
			// return {
			// 	events: [
			// 		{
			// 			id: '123',
			// 			title: 'Duis autem vel eum iriure dolor',
			// 			start_date: 'test',
			// 			description: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.',
			// 		},
			// 		{
			// 			id: '124',
			// 			title: 'Ut wisi enim ad minim veniam, quis nostrud',
			// 			start_date: 'test2',
			// 			description: 'Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.',
			// 		},
			// 		{
			// 			id: '125',
			// 			title: 'Sed diam nonummy nibh euismod tincidunt ut laoreet dolore',
			// 			start_date: 'test2',
			// 			description: 'Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum.',
			// 		}
			// 	]
			// };
		},
		components: {
			ControlColumn,
			EventListing,
			PageHeader,
			MapView,
			EventResults
		}
	};
</script>
