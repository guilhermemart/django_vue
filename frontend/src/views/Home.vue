<template>
    <div>
        <harpiaBar />
        <div class="home">

    <div class="columns is-multiline">
      <alert_card
        v-for="alert in latest_alerts"
        v-bind:key="alert.id"
        v-bind:Alert="alert" />
    </div>
  </div>
    </div>

</template>

<script>
import alert_card from '@/components/alert_card.vue'
import axios from 'axios'
import harpiaBar from '@/components/harpiaBar.vue'


export default {
    name: 'Alerts',
  components:{
    harpiaBar,
    alert_card
  },
  data() {
    return {
        latest_alerts: [],
        page: "1"
    }
  },

  mounted() {
    this.get_latest_alerts()
    document.title = 'Alerts | Harpia'
  },
    methods: {
    watchdog() {

    },
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
