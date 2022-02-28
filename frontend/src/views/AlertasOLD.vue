<template>
<div>
<harpiaBar />

  <div class="home">
  <section class="hero is-medium is-dark mb-6">
        <div class="hero-body has-text-centered">
            <p class="title mb-6">
                Bem vindo ao Harpia
            </p>
            <p class="subtitle">
                Versão beholder
            </p>
        </div>
  </section>
    <div class="columns is-multiline">
      <div class="column is-12">
          <h2 class="is-size-2 has-text-centered">Latest Alerts</h2>
      </div>
      <alert_card
        v-for="alert in latest_alerts"
        v-bind:key="alert.id"
        v-bind:Alert="alert" />
    </div>
  </div>
  </div>
  </template>
<style lang="scss">

</style>

<script>

import alert_card from '@/components/alert_card.vue'
import axios from 'axios'
import harpiaBar from '@/components/harpiaBar.vue'
export default {  
  name: 'Alerts',
  components:{
    harpiaBar
  },
  data() {
    return {
        latest_alerts: []
    }
  },
  components: {
    alert_card
  },
  mounted() {
    this.get_latest_alerts()
    document.title = 'Alerts | Harpia'
  },
    methods: {
    async get_latest_alerts() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get('/api/v1/latest-alerts/1')
        .then(response => {
          this.latest_alerts = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>
