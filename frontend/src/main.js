import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
//monta esse App no public-->index.html
createApp(App).use(store).use(router).mount('#app')
