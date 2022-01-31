import { createApp } from 'vue'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'
import Konva from "konva";
import VueKonva from "vue3-konva";

// magia pra nao precisar chamar a api pelo endereço completo
axios.defaults.baseURL = 'http://127.0.0.1:8000'

//monta esse App no public-->index.html
//createApp(App).use(store).use(router).mount('#app')
const app = createApp(App);
app.use(store);
app.use(router, axios);
app.use(VueKonva);
app.use(Konva);
app.mount('#app');