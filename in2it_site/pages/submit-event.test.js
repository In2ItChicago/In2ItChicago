import { resolve } from 'path';
import { Nuxt, Builder } from 'nuxt';
import request from 'supertest';



// We keep the nuxt and server instance
// So we can close them at the end of the test
let nuxt = null

// Init Nuxt.js and create a server listening on localhost:4000
beforeAll(async () => {
  const config = {
    dev: process.env.NODE_ENV === 'production',
    rootDir: resolve(__dirname, '../'),
    mode: 'universal',
  }

  nuxt = new Nuxt(config)

  await new Builder(nuxt).build()

  await nuxt.server.listen(3000, 'localhost')
}, 30000)

// Example of testing only generated html
// describe('GET /', () => {
//   test('Route / exits and render HTML', async () => {
//     const { html } = await nuxt.renderRoute('/', {})

//     expect(html).toContain('welcome')
//   })
// })

test(()=> {
    expect(1+1).toBe(2)
})


afterAll(() => {
  nuxt.close()
})