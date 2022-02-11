<template>
    <div>
      <harpiaBar />
     <div class="hero has-background-grey-lighter is-fullheight-with-navbar">
    
   
  <!-- <div class="level-item has-text-centered mt-4">
    <div class="calendar">
       <Datepicker v-model="date" :format="format" autoApply :enableTimePicker="false" calendarCellClassName="dp-custom-cell" />  
       <button class="button has-text-light has-custom-width is-medium is-responsive is-success">Find<span class="is-family-sans-serif"></span></button>     
    </div>
  </div> -->

  <div class="has-addons level-item has-text-centered mt-4">
  <div class="control calendar">
  
   <Datepicker v-model="date" :format="format" autoApply :enableTimePicker="false" calendarCellClassName="dp-custom-cell" placeholder="Select a Date"></Datepicker>  
  </div>
  <div class="control">    
       <button class="button ml-2 has-text-light has-custom-width is-medium is-responsive is-primary">Confirm<span class="is-family-sans-serif"></span></button>     
  </div>
  <div class="control">    
       <button class="button ml-2 has-text-light has-custom-width is-medium is-responsive is-primary">Refresh<span class="is-family-sans-serif"></span></button>     
  </div>
  
</div>


      <div v-if="false">
        <div class="control">
          <label class="radio">
            <input v-model="isRange" value="false" type="radio" name="day">
            dia
          </label>
          <label class="radio">
            <input v-model="isRange" value="false" type="radio" name="period">
            periodo
          </label>
        </div>
        
      
      {{date}}
      <hr>
      {{isRange}}
      </div>
        <div class="home">

    <div class="columns mt-4 is-centered">
                        <div class="column">
                            <b-button size="is-large" @click="CurrentPage -= 1" icon-right="chevron-left" type="is-primary" :disabled="CurrentPage <= 1" outlined />
                        </div>
                            <div class="column is-12">
                            <!--div class="columns has-text-black is-multiline" v-if="GetCurrentPageAlerts.length 0"-->
                            <div class="columns has-text-black is-multiline mr-2" v-if="true">
                                <div class="column is-6" v-for="alert in latest_alerts" v-bind:key="alert.id">
                                    <div>
                                    <alert_card :Alert="alert" />
                                    </div>
                                </div>
                            </div>
                            <div class="column is-12 has-text-centered is-half-screen-height is-flex has-vertical-centered-text" v-else>
                                <b-icon icon="alert" size="is-large" type="is-dark">
                                </b-icon>
                                <p class="title">
                                    Não há alertas disponíveis.
                                </p>
                            </div>
                        </div>
    
    </div>




    <div class="columns is-multiline" v-if="false">
      <alert_card
        v-for="alert in latest_alerts"
        v-bind:key="alert.id"
        v-bind:Alert="alert" />
    </div>
  </div>
  
    </div>
    </div>
</template>
<style lang="scss">

.dp-custom-cell {
  border-radius: 50%;
  
};
.calendar input{
  width: 250px;
  height: 50px;  
  text-align: center;  
};
.btn{
  border-radius: 5vh;
}



</style>
<script>
import alert_card from '@/components/alert_card.vue'
import axios from 'axios'
import harpiaBar from '@/components/harpiaBar.vue'

import { ref } from "vue";
import Datepicker from "vue3-date-time-picker";
import "vue3-date-time-picker/dist/main.css";


export default {
    name: 'Alerts',

  components:{
    Datepicker,
    harpiaBar,
    alert_card
  },
  data() {
    return {
        latest_alerts: [],
        page: "1",

        date: new Date(),
        last_date: new Date(),
        isRange:'',
        format:'',
        
    }
  },
   setup() {
        const date = ref();
        // In case of a range picker, you'll receive [Date, Date]
        const format = (date) => {
            const day = String(date.getDate()).length <2? '0'+String(date.getDate()):String(date.getDate())
            const month = String(date.getMonth() + 1).length <2? '0'+String(date.getMonth() + 1):String(date.getMonth() + 1);
            const year = date.getFullYear();

            



            return `${day}/${month}/${year}`;
        }
        
        return {
            date,
            format,
        }
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
