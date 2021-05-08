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
      {
        hid: 'description',
        name: 'description',
        content:
          'Make an impact in your Neighborhood, Community and City in Chicagoland. Find ways to get civically involved, contribute your skills, make a difference.',
      },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/img/favicon.jpg' },
      { rel: 'stylesheet', href: '/css/style.css' },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css?family=Nunito&display=swap',
      },
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap',
      },
    ],
    script: [
      {
        src: 'https://www.googletagmanager.com/gtag/js?id=UA-152726306-1',
        type: 'text/javascript',
      },
      {
        innerHTML:
          "window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'UA-152726306-1');",
        type: 'text/javascript',
      },
    ],
  },

  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },

  /*
   ** Global CSS
   */
  css: [],

  /*
   ** Plugins to load before mounting the App
   */
  // don't load firebase plugin if env var isn't set
  // var won't be there during prod build so only check during dev builds
  plugins: [
    { src: '~/plugins/notifications.client.js' },
    { src: '~/plugins/firebase.js' },
  ].filter(
    (o) =>
      !o.src.endsWith('firebase.js') ||
      process.env.FIREBASE_API_KEY ||
      process.env.NODE_ENV !== 'development'
  ),

  /*
   ** Nuxt.js modules
   */
  modules: [
    // Doc: https://github.com/nuxt-community/axios-module#usage
    '@nuxtjs/axios',
    // Doc: https://bootstrap-vue.js.org/docs/
    'bootstrap-vue/nuxt',
    '@nuxtjs/vuetify',
    [
      'nuxt-env',
      {
        keys: [
          'IN2IT_API_URL',
          'FIREBASE_API_KEY',
          'FIREBASE_AUTH_DOMAIN',
          'FIREBASE_DATABASE_URL',
          'FIREBASE_PROJECT_ID',
          'FIREBASE_STORAGE_BUCKET',
          'FIREBASE_MESSAGING_SENDER_ID',
          'FIREBASE_APP_ID',
          'FIREBASE_MEASUREMENT_ID',
        ],
      },
    ],
    [
      'nuxt-google-maps-module',
      {
        key: 'AIzaSyDKuKo2WRNv5IhKm_At8wGfD4T142laung',
      },
    ],
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
      cacheDirectory: '/usr/src/app/.site_modules',
    },
    extend(config, { isClient }) {
      if (isClient) config.devtool = '#eval-source-map'
      else config.devtool = '#inline-source-map'
      return config
    },
    devtools: true,
  },
  watchers: {
    webpack: {
      aggregateTimeout: 300,
      poll: 1000,
      ignored: /node_modules/,
    },
  },
  router: {
    scrollBehavior: async (to, from, savedPosition) => {
      if (savedPosition) {
        return savedPosition
      }

      const findEl = async (hash, x) => {
        return document.querySelector(hash) ||
          new Promise((resolve, reject) => {
            if (x > 50) {
              return resolve()
            }
            setTimeout(() => { resolve(findEl(hash, ++x || 1)) }, 100)
          })
      }

      if (to.hash) {
        let el = await findEl(to.hash)
        if ('scrollBehavior' in document.documentElement.style) {
          return window.scrollTo({ top: el.offsetTop, behavior: 'smooth' })
        } else {
          return window.scrollTo(0, el.offsetTop)
        }
      }

      return { x: 0, y: 0 }
    }
  }
}
