<template>
    <div>
      <harpiaBar :show_in_bar="true"/>
     <div class="hero has-background-grey-lighter is-fullheight-with-navbar">

  <!-- <div class="level-item has-text-centered mt-4">
    <div class="calendar">
       <Datepicker v-model="date" :format="format" autoApply :enableTimePicker="false" calendarCellClassName="dp-custom-cell" />  
       <button class="button has-text-light has-custom-width is-medium is-responsive is-success">Find<span class="is-family-sans-serif"></span></button>     
    </div>
  </div> -->
<div v-if="true">
        <div class="control mt-1">
          <label class="radio">
            <input v-model="isRange" v-bind:value="true" type="radio" name="day">
            dia
          </label>
          <label class="radio">
            <input v-model="isRange" v-bind:value="false" type="radio" name="period">
            periodo
          </label>
        </div>

      </div>
  <div class="has-addons level-item has-text-centered ">
  
  <div class="control calendar" v-if="isRange">  
    <Datepicker v-model="date" :format="format" autoApply :enableTimePicker="false" calendarCellClassName="dp-custom-cell" placeholder="Select a Date" />   
  </div>

  <div class="control calendar" v-else>
  <Datepicker v-model="date" autoApply range :enableTimePicker="false" calendarCellClassName="dp-custom-cell" placeholder="Select a period" />
  </div>


  <div class="control">    
       <button class="button ml-2 has-text-light has-custom-width is-medium is-responsive is-primary" :disabled="date==''" @click="findALerts()">Confirm<span class="is-family-sans-serif"></span></button>     
  </div>
  <div class="control">    
       <button class="button ml-2 has-text-light has-custom-width is-medium is-responsive is-primary" @click="refreshPage()">Refresh<span class="is-family-sans-serif"></span></button>     
  </div>
  
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
    <nav class="pagination" role="navigation" aria-label="pagination">
        <a v-if="page>1" class="pagination-previous" @click="go_to_page(parseInt(page)-1)"><router-link to="'/latest-alerts/'+ ((parseInt(page)-1).toString()">Previous</router-link></a>
        <a v-if="has_next_page == true" class="pagination-next" @click="go_to_page(parseInt(page)+1)"><router-link to="'/latest-alerts/'+ ((parseInt(page)+1).toString()">Next</router-link></a>
    </nav>
{{page}}
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
    harpiaBar,
    alert_card,
    Datepicker,
  },
  data() {
    return {
        latest_alerts: [],
        page: "1",
        date:'',
        last_date: new Date(),
        isRange:true,
        format:'',
        has_next_page: false,
    }
  },
    computed: {
 

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
    this.page=this.$route.params.page  // armazena em qual pagina está
    this.get_latest_alerts(),
    document.title = 'Alerts | Harpia'
  },
  created(){
    this.watchdog()
    this.date=''
  },
  watch:{    
  isRange:{
    handler(){      
      this.date=""
    }  
  }  
  },
  methods: {
    play_audio(vol){
        if(this.$store.state.audio.is_on==true){
            var audio = new Audio(require("../assets/beep-12.wav"));
            audio.volume = vol
            audio.play()
        }
    },
    watchdog(){
        axios.get('/api/v1/watchdog').then( item => {
            if(this.page == '1'){
                this.get_latest_alerts()
                console.log("watchdog atuando")
            }
            if(this.$store.state.audio.is_instantaneo == true){
                this.play_audio(1)
            }
            this.watchdog()
        })
    },
    async get_latest_alerts() {
      this.$store.commit('setIsLoading', true)
      let data= {
        "end": this.$store.state.filter.date_end,
        "valids": this.$store.state.filter.valid,
        "invalids": this.$store.state.filter.invalid,
        "non_classifieds": this.$store.state.filter.non_classified,
        "start": this.$store.state.filter.date_start,
      }
      await axios
        .post('/api/v1/latest-alerts/'+this.page, data)
        .then(response => {
          this.latest_alerts = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
      if(Object.keys(this.latest_alerts).length>6){
        this.has_next_page = true
        this.latest_alerts = this.latest_alerts.slice(0,6)
      }
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
    refreshPage(){
       this.watchdog()
    this.date=''
    this.get_latest_alerts()
    

    },
    findALerts(){      
      if(this.isRange){
        //Extrai apenas a data
        let day= new Date(this.date).toDateString()
        //Gera o timestamp da data as 00:00:00 horas
        let timestamp= new Date(day).getTime()
        
        console.log(timestamp)
        
      }else{
        //Extrai apenas a data
        let day0= new Date(this.date[0]).toDateString()
        let day1= new Date(this.date[1]).toDateString()
        //Gera o timestamp da data as 00:00:00 horas
        let timestamp0= new Date(day0).getTime()
        let timestamp1= new Date(day1).getTime()
        
        console.log(timestamp0)
        console.log(timestamp1)
        
      }
      

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
