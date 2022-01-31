import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'





import axios from 'axios'

require("./styles/harpia.scss")
// magia pra nao precisar chamar a api pelo endereço completo
//axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.baseURL = 'http://192.168.0.27:8000'

//monta esse App no public-->index.html
//createApp(App).use(store).use(router).mount('#app')
createApp(App).use(store).use(router, axios).mount('#app')