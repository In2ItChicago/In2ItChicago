const pkg = require('./package')

module.exports = {
	mode: 'universal',

	/*
	** Headers of the page
	*/
	head: {
		title: 'In2It Chicago',
		meta: [
			{ charset: 'utf-8' },
			{ name: 'viewport', content: 'width=device-width, initial-scale=1' },
			{ hid: 'description', name: 'description', content: pkg.description }
		],
		link: [
			{ rel: 'icon', type: 'image/x-icon', href: '/img/favicon.jpg' },
			{ rel: 'stylesheet', href: '/css/style.css' },
			{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Nunito&display=swap' },
			{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap' }
		],
		script: [
			{ src: 'https://www.googletagmanager.com/gtag/js?id=UA-152726306-1', type: 'text/javascript' },
			{ innerHTML: "window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'UA-152726306-1');", type: 'text/javascript'}
		],
	},

	/*
	** Customize the progress-bar color
	*/
	loading: { color: '#fff' },

	/*
	** Global CSS
	*/
	css: [
        
	],

	/*
	** Plugins to load before mounting the App
	*/
	plugins: [
		{src: '~/plugins/datepicker.client.js'},
		{src: '~/plugins/notifications.client.js'},
		{src: '~/plugins/pagination.client.js'},
	],

	buildModules: [
		'@nuxtjs/vuetify',
	],

	/*
	** Nuxt.js modules
	*/
	modules: [
		// Doc: https://github.com/nuxt-community/axios-module#usage
		'@nuxtjs/axios',
		// Doc: https://bootstrap-vue.js.org/docs/
		'bootstrap-vue/nuxt',
		['nuxt-env', {
			keys: ['IN2IT_API_URL']
		}],
		['nuxt-google-maps-module', {
			key: 'AIzaSyDKuKo2WRNv5IhKm_At8wGfD4T142laung',
		}],
	],
	/*
	** Axios module configuration
	*/
	axios: {
		// See https://github.com/nuxt-community/axios-module#options
	},

	/*
	** Build configuration
	*/
	build: {
		/*
		** You can extend webpack config here
		*/
		babel: {
			cacheDirectory: '/usr/src/app/.site_modules'
		},
		extend(config, { isClient }) {
            if (isClient)
				config.devtool = '#eval-source-map'
			else
				config.devtool = '#inline-source-map'
            return config;
		},
		devtools: true
	},
    watchers: {
        webpack: {
            aggregateTimeout: 300,
            poll: 1000,
            ignored: /node_modules/
        }
    }
}
