import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from '@/App.vue'
import router from '@/router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHeart as fasHeart } from '@fortawesome/free-solid-svg-icons'
import { faHeart as farHeart } from '@fortawesome/free-regular-svg-icons'

library.add(fasHeart, farHeart)

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)


const pinia = createPinia()
app.use(pinia)


app.use(router)

app.mount('#app')

