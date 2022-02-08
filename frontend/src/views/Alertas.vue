<template>
    <div>
        <harpiaBar />
        <!--calendar_search/-->
        <div class="home">

  <div>
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
    <Datepicker v-model="date" :range="isRange" :partialRange='false'/>
    {{date}}
    <hr>
    {{isRange}}
  </div>

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
//import calendar_search from '@/components/calendar_search.vue'
import { ref } from "vue";
import Datepicker from "vue3-date-time-picker";
import "vue3-date-time-picker/dist/main.css";
export default {
  name: 'Alerts',
  components:{
    //calendar_search,
    harpiaBar,
    alert_card,
    Datepicker,
  },
  data() {
    return {
        latest_alerts: [],
        page: "1",
        date: new Date(),
        last_date: new Date(),
        isRange:'',
        audio: {
            is_on: true,
            is_instantaneo: true,
            is_recorrente: true,
            has_delay: true
        }
    }
  },
  computed:{
    dateSelect(){
      return this.date
    }
  },
  watch:{
      dateSelect:{
        handler(){
          this.toTimestamp()
        }
      },
      watchdog:{
           handler(){
               this.watchdog
           }
      }
  },
  mounted() {
    this.page=this.$route.params.page  // armazena em qual pagina está
    this.get_latest_alerts(),
    this.audio = this.$store.state.audio
    document.title = 'Alerts | Harpia'
  },
  created(){
    this.watchdog()
  },
  methods: {
    watchdog(){
        axios.get('/api/v1/watchdog').then( item => {
            if(this.page == '1'){
                this.get_latest_alerts()
                console.log("watchdog atuando")
                this.play_audio(1)
                }
            this.watchdog()
            })
        },
    play_audio(vol){
            if (this.audio.is_on==true && this.audio.is_instantaneo==true){
            var audio = new Audio(require("../assets/beep-12.wav"));
            audio.volume = vol
            audio.play()}
        },
    async get_latest_alerts() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get('/api/v1/latest-alerts/'+this.page)
        .then(response => {
          this.latest_alerts = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    },
    async get_date_filtered_alerts() {
      this.$store.commit('setIsLoading', true)
      var path='/api/v1/'+this.date[0]+'/'+this.date[1]+'/'+this.page
      alert(path)
      await axios
        .get('/api/v1/alert_search/'+this.date[0]+'/'+this.date[1]+'/'+this.page)
        .then(response => {
          this.latest_alerts = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    },
    toTimestamp(){
      let justDate0=new Date(this.date[0]).toDateString()
      this.date[0]=new Date(justDate0).getTime()
      let justDate1=new Date(this.date[1]).toDateString()
      this.date[1]=new Date(justDate1).getTime()-99
      console.log(this.get_date_filtered_alerts())
    },
  },
}
</script>
