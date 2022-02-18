<template>
  <div class="resumo_page">
    <harpiaBar/>

    <div class="hero has-background-grey-lighter is-fullheight-with-navbar">
      <div class="columns mt-6 is-centered">
        <resumo_card class="column is-3 is-size-4"/>
        <resumo_card class="column is-3 is-size-4"/>
        <resumo_card class="column is-3 is-size-4"/>
      </div>
    </div>



  </div>
</template>

<script>
import harpiaBar from '@/components/harpiaBar.vue'
import Resumo_card from "@/components/resumo_card"
import axios from 'axios'

export default {
  name: "Resumo",
  components: {
    Resumo_card,
    harpiaBar
  },
  data() {
    return {
      alerts: [],
    }
  },
  mounted() {
    this.getAlerts()
  },
  methods: {
    async getAlerts() {
      await axios
          .get('/api/v1/alerts/all')
          .then(response => {
            this.alerts = response.data
            console.log(this.alerts)
          })
      .catch(error => {
        console.log(error)
      })
    },


  }

}
</script>

<style scoped>

</style>