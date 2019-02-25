<template>
    <div>
        <h1>{{ event.title }}</h1>
        <p>{{ event.description }}</p>
    </div>
</template>


<script>
    import axios from 'axios';
	import rest from '@feathersjs/rest-client';
	import feathers from '@feathersjs/feathers';
    
    const app = feathers();
	const restClient = rest('http://event_service:5000');
	app.configure(restClient.axios(axios));
    const events = app.service('events');

    export default{
        data() {
			return {
				event: []
			};
		},
		asyncData ({params}) {
			return events.find({query: {id: params.id}})
				.then(res => {
					return { event: res.data };
				});
		}
    };
</script>