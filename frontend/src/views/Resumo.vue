<template>
  <div class="resumo_page">
    <harpiaBar/>

    <div class="hero has-background-grey-lighter is-fullheight-with-navbar mg-large">
      <div class="columns is-centered hero-body">
        <resumo_card class="column is-3 is-size-4" v-bind:monthly-data="pastMonth"/>
        <resumo_card class="column is-3 is-size-4" v-bind:monthly-data="thisMonth"/>
        <resumo_card class="column is-3 is-size-4" v-bind:monthly-data="today"/>
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
      today: [],
      thisMonth: [],
      pastMonth: []
    }
  },
  mounted() {
    this.getAlerts()
  },
  methods: {
    /* Pega os dados do 'alerts/report' e salva em variáveis separadas, uma pra cada card */
    async getAlerts() {
      await axios
          .get('/api/v1/alerts/report')
          .then(response => {
            this.today = response.data.today
            this.thisMonth = response.data.now
            this.pastMonth = response.data.past
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