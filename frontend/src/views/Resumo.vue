<template>
  <div class="resumo_page">
    <harpiaBar/>

    <div class="hero has-background-grey-lighter is-fullheight-with-navbar">
      <div class="columns mt-6 is-centered">
        <resumo_card class="column is-3 is-size-4" v-bind:monthly-data="pastMonth"/>
        <resumo_card class="column is-3 is-size-4" v-bind:monthly-data="thisMonth"/>
        <resumo_card class="column is-3 is-size-4" v-bind:monthly-data="thisMonth"/>
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
      thisMonth: [],
      pastMonth: []
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