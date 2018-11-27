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
    import { dummyData } from '~/store/dummydata.js';

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
            if (process.env.DUMMY_DATA) {
                return { events: dummyData };
            }
			return events.find({query: {start_timestamp: 0, end_timestamp: 10000000000000}})
				.then(res => {
					return { events: res.data };
				});
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
