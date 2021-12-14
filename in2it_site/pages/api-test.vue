<template>
    <div class="container">
        <div class="content-col col-md-8 offset-md-2 col-sm-12">
            <h1>API Test</h1>

			<v-label>
				Endpoint URL
				<span class="required-star"> *</span>
			</v-label>
			<v-text-field
				v-model="endpointUrl"
				outlined
			></v-text-field>

			<v-label>
				Payload
				<span class="required-star"> *</span>
			</v-label>
			<v-textarea
				v-model="payload"
				outlined
			></v-textarea>

			<v-btn color="#173450" @click="postToAPI" dark large>Post</v-btn>
        </div>
    </div>
</template>

<script lang='ts'>
	import axios from 'axios';
    import firebase from 'firebase/app'
    import 'firebase/auth'

	export default {
		data() {
			return {
				endpointUrl: '/end-point',
				payload: '{"key": "value"}'
			};
		},
		methods: {
			postToAPI: async function () {
				let token = '';
				const auth = await firebase.auth();
                if (auth.currentUser) {
                    token = await auth.currentUser.getIdToken();
                }
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
				console.log(JSON.parse(this.payload));
                axios.post(this.endpointUrl, JSON.parse(this.payload), config)
                .then((res) => {
                    console.log('API Response', res);
                    alert('Success');
                })
                .catch((err) => {
                    alert(err);
                });
			}
		}
	};
</script>