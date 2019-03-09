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
			{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
			{ rel: 'stylesheet', href: '/css/style.css' },
			{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Signika' },
			{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Signika' },
			{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Kalam' },
			{ rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Permanent+Marker' }
		]
	},

	/*
	** Customize the progress-bar color
	*/
	loading: { color: '#fff' },

	/*
	** Global CSS
	*/
	css: [
        '@/node_modules/bootstrap/dist/css/bootstrap.css'
	],

	/*
	** Plugins to load before mounting the App
	*/
	plugins: [
	],

	/*
	** Nuxt.js modules
	*/
	modules: [
		// Doc: https://github.com/nuxt-community/axios-module#usage
		'@nuxtjs/axios',
		// Doc: https://bootstrap-vue.js.org/docs/
        'bootstrap-vue/nuxt',
        'nuxt-typescript'
	],
	env: {
		API_URL: process.env.API_URL || 'api.localhost'
	},
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
		extend(config, ctx) {
            if (process.env.NODE_ENV === 'dev') {
                if (ctx.isClient)
                    config.devtool = 'eval-source-map'
                else
                    config.devtool = 'inline-source-map'
            return config;
            }
		}
    },
    watchers: {
        webpack: {
            aggregateTimeout: 300,
            poll: 1000,
            ignored: /node_modules/
        }
    }
}
