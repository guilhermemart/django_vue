<template>
    <div>
      <harpiaBar :show_in_bar="true"/>
        <div class="hero has-background-grey-lighter is-fullheight-with-navbar">
        <div class="home mb-2">
        <div class="columns is-vcentered">
        <div class="column is-multiline is-mobile">
            <button class="button is-outlined is-rounded is-large is-inverted" @click="go_to_page(parseInt(page)-1)" :disabled="page<2" > <i class="fas fa-angles-left fa-2x" /></button>
        </div>
        <div class="column is-10">
        <div>
        <div class="control mt-1">
            <label class="radio">
            <input v-model="isRange" v-bind:value="true" type="radio" name="day">
            day
            </label>
            <label class="radio">
            <input v-model="isRange" v-bind:value="false" type="radio" name="period">
            period
            </label>
        </div>
        <div class="has-addons level-item has-text-centered ">
          <div class="control calendar" v-if="isRange">
              <Datepicker v-model="date" :format="format" autoApply :enableTimePicker="false" calendarCellClassName="dp-custom-cell" :placeholder="date" />
          </div>
          <div class="control calendar" v-else>
              <Datepicker v-model="date" autoApply range :enableTimePicker="false" calendarCellClassName="dp-custom-cell" :placeholder="date" />
          </div>
          <div class="control">
            <button class="button ml-2 has-text-light has-custom-width is-medium is-responsive is-primary" :disabled="placeHolder==date" @click="findALerts()">
              <span class="icon">
                  <i class="fas fa-search"></i>
              </span>
            <span class="is-family-sans-serif">Confirm</span></button>
          </div>
          <div class="control">
            <button class="button ml-2 has-text-light has-custom-width is-medium is-responsive is-primary" @click="refreshPage()">
            <span class="icon">
            <i class="fas fa-sync"></i>
            </span>
            <span class="is-family-sans-serif">Reset</span></button>
          </div>
        </div>
    </div>
          <div class="mt-4">Page {{page}}</div>
          <!--div class="columns has-text-black is-multiline" v-if="GetCurrentPageAlerts.length 0"-->
          <div class="columns has-text-black is-multiline mr-2 mt-3" v-if="true">
            <!--  <div class="column is-6" v-for="alert in latest_alerts" v-bind:key="alert.id"> -->
              <div class="column is-6" v-for="alert in latest_alerts" v-bind:key="alert.timestamp">
                  <div>
                  <alert_card :Alert="alert" />
                  <!-- {{new Date(alert.date_added).toLocaleString()}}
                  {{alert.anotacoes}} -->
                  </div>
              </div>
          </div>
          <div class="column is-12 has-text-centered is-half-screen-height is-flex has-vertical-centered-text" v-else>
              <i icon="alert" size="is-large" type="is-dark"></i>
              <p class="title">
                  No alerts available.
              </p>
          </div>
        </div>
        <div class="column is-multiline is-mobile">
            <button class="button is-outlined is-rounded is-large is-inverted" @click="go_to_page(parseInt(page)+1)">
            <i class="fas fa-angles-right fa-2x" />
            </button>
        </div>
    </div>
    <div class="columns is-multiline" v-if="false">
      <alert_card
        v-for="alert in latest_alerts"
        v-bind:key="alert.id"
        v-bind:Alert="alert" />
    </div>
    <!-- <nav class="pagination" role="navigation" aria-label="pagination">
        <a v-if="page>1" class="pagination-previous" @click="go_to_page(parseInt(page)-1)">Previous</a>
        <a v-if="has_next_page == true" class="pagination-next" @click="go_to_page(parseInt(page)+1)"> <button>Next</button> </a>
    </nav> -->
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

import axios from 'axios'
import { ref } from "vue";
import Datepicker from "vue3-date-time-picker";
import "vue3-date-time-picker/dist/main.css";
// componentes customizados
import alert_card from '@/components/alert_card.vue'
import harpiaBar from '@/components/harpiaBar.vue'

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
        date:'DATA SET',
        last_date: new Date(),
        isRange:true,
        format:'',
        has_next_page: false,
        CurrentPage:1,
        filter:{
            date_end: 2500916953418,
            valid: true,
            invalid: true,
            non_classified: true,
            date_start: 0,
        },
        confirmDisable: true,
        placeHolder: ""
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
    this.filter = this.$store.state.filter
    // para mostrar a data/periodo selecionado
    if (this.filter.date_start === 0) {
      this.date = "Filter by date"
      this.placeHolder = this.date
    } else if (this.filter.date_end - this.filter.date_start !== 86399999) {
      this.isRange = false
      let date_0 = new Date(this.filter.date_start)
      let date_1 = new Date(this.filter.date_end)
      this.date =  (date_0.getMonth() + 1) + "/" + date_0.getDate() + "/" + date_0.getFullYear() + " - "
      this.date = this.date + (date_1.getMonth() + 1) + "/" + date_1.getDate() + "/" + date_1.getFullYear()
      this.placeHolder = this.date
    }
    else {
      this.date = new Date(this.filter.date_start)
      this.placeHolder = this.date
    }


    //this.$store.state.filter=this.filter
    this.get_latest_alerts()
    document.title = 'Alerts | Harpia' //  titulo do documento para diferenciar dos outros .vue
  },
  created(){
    this.watchdog()

  },
  watch:{    
  isRange:{
    handler(){
      // para mostrar as datas selecionadas ou "filter by date" quando troca pra day/period
      if (this.filter.date_start === 0) {
        this.date = "Filter by date"
        this.placeHolder = this.date
      } else if (this.isRange && this.filter.date_end - this.filter.date_start !== 86399999) {
        this.date = "Filter by date"
        this.placeHolder = this.date
      } else if (!this.isRange && this.filter.date_end - this.filter.date_start !== 86399999) {
        let date_0 = new Date(this.filter.date_start)
        let date_1 = new Date(this.filter.date_end)
        this.date =  (date_0.getMonth() + 1) + "/" + date_0.getDate() + "/" + date_0.getFullYear() + " - "
        this.date = this.date + (date_1.getMonth() + 1) + "/" + date_1.getDate() + "/" + date_1.getFullYear()
        this.placeHolder = this.date
      } else if (!this.isRange && this.filter.date_end - this.filter.date_start === 86399999) {
        this.date = "Filter by date"
        this.placeHolder = this.date
      } else if (this.isRange && this.filter.date_end - this.filter.date_start === 86399999) {
        this.date = new Date(this.filter.date_start)
        this.placeHolder = this.date
      }

      //this.date=""
    },
  watchdog: {
    handler(){
        this.watchdog
    }
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
            }
            if(item.data == "1" && this.$store.state.audio.is_instantaneo === true){
                this.play_audio(1)
            }
            this.watchdog()
        })
    },
    get_latest_alerts() {
      axios
        .post('/api/v1/latest-alerts/'+this.page, this.filter)
        .then(response => {
          console.log(this.filter)
          this.latest_alerts = response.data
      if(Object.keys(this.latest_alerts).length>6){        
        this.has_next_page = true  // usado para paginacao
        this.latest_alerts = this.latest_alerts.slice(0,6)
        }
        })
        .catch(error => {
          console.log(error)
        })
    },
    go_to_page(next_page){ // usada na paginacao
        console.log("teste")
        // router push nao reloada a pagina se mudar apenas o parametro
        this.$router.push("/latest-alerts/"+next_page.toString()).then(
        ()=> {  // push manda pra proxima pagina --> similar router-link
        this.$router.go()  // forca o reload da pagina --> router.push tem problema nisso
        })
    },
    refreshPage(){
        this.filter.date_start = 0
        this.filter.date_end = 2500916953418
        this.$store.commit("save_filter", this.filter)
        this.$router.push("/latest-alerts/1").then(()=> {
            this.$router.go()
        })
    },
    findALerts(){      
      if(this.isRange){
        //Extrai apenas a data
        let day= new Date(this.date).toDateString()
        //Gera o timestamp da data as 00:00:00 horas
        let timestamp= new Date(day).getTime()
        
        // timestamp incluso no filtro        
        this.filter.date_start =timestamp
        this.filter.date_end= new Date(timestamp).setHours(23,59,59,999)
        this.$store.commit('save_filter', this.filter)
      }else{
        //Extrai apenas a data
        let day0= new Date(this.date[0]).toDateString()
        let day1= new Date(this.date[1]).toDateString()
        //Gera o timestamp da data as 00:00:00 horas
        let timestamp0= new Date(day0).getTime()
        let timestamp1= new Date(new Date(day1).setHours(23,59,59,999)).getTime()

        // timestamp incluso no filtro
        this.filter.date_start=timestamp0
        this.filter.date_end=timestamp1
        this.$store.commit('save_filter', this.filter)
      }

      this.$router.push("/latest-alerts/1").then(()=> {
            this.$router.go()
        })
      this.get_latest_alerts()
    }
  },
}
</script>
