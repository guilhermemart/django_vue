import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'
// magia pra nao precisar chamar a api pelo endereço completo
//axios.defaults.baseUrl = 'http://127.0.0.1:8000'

//monta esse App no public-->index.html
createApp(App).use(store).use(router, axios).mount('#app')
