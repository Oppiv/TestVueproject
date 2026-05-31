import { createApp } from 'vue'
import App from './App.vue'
import { createVuetify } from 'vuetify/lib/entry-bundler.mjs'
import 'vuetify/styles'

const app = createApp(App)
const vuetify = createVuetify()


app.use(vuetify)
app.mount('#app')
