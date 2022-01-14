<template>
  <div class="box has-background-white">  
    
    <div class="has-text-right mb-4">
      <b-button v-if= "get_thumb_up() == 'true'" size="is-small" icon-right="thumb-up" class="is-floating-right" rounded inverted type= 'is-success' @click="invert_thumb_up()" /> 
      <b-button v-else size="is-small" icon-right="thumb-up" class="is-floating-right"  rounded inverted  @click="invert_thumb_up()"/> 
      <b-button v-if= "get_thumb_down() == 'true'" size="is-small" icon-right="thumb-down" class="is-floating-left" rounded inverted  type= 'is-danger' @click="invert_thumb_down()"/> 
      <b-button v-else size="is-small" icon-right="thumb-down" class="is-floating-left"  rounded inverted  @click="invert_thumb_down()" /> 
      <b-button size="is-small" icon-right="message" class="is-observation" rounded inverted 
      :type="{'is-link':Alert.notes,'is-dark':!Alert.notes}" @click="insertObservation()" /> 
      
    </div>
    <div class="columns is-paddingless">
      <div class="column is-4 has-text-left">
        <div class="container has-text-underlined">
          <b-icon  class="has-right-space" icon="hard-hat" type="is-primary"></b-icon>
          <span  class="is-size-6 has-text-weight-bold has-text-primary">{{ Alert.alerts[0] }} EPI</span>
        </div>

        <div class="container has-text-underlined">
          <b-icon class="has-right-space" icon="exclamation-thick" type="is-primary"></b-icon>
          <span class="is-size-6 has-text-weight-bold has-text-primary">{{ Alert.alerts[1] }} Red Zone</span>
        </div>

        <span class="has-text-grey-light is-custom-size">ID: {{ Object.values(this.Alert._id)[0] }}</span>
      </div>
      <div class="column is-3">
        <AlertCardBox :Label="'Data'" :Data="new Date(Object.values(Alert.datetime)[0]).toLocaleDateString('pt-BR')"/>
        <AlertCardBox :Label="'Hora'" :Data="new Date(Object.values(Alert.datetime)[0]).toLocaleTimeString('pt-BR')"/>

        
      </div>
      
      <div class="column is-5">
        <img id="file" @click="IsImageModalActive = true" class="has-pointer-cursor" :src="get_alert_image()"/>
      </div>
    </div>
    <b-modal v-model="IsImageModalActive">
      <img :src="get_alert_image()" alt="Imagem do alerta"/>
    </b-modal>
    <b-modal v-model="showObservationModal" has-modal-card trap-focus>
        <div class="modal-card" style="width: 120vh">
          <header class="modal-card-head">
            <p class="modal-card-title">Observações  <span class="is-size-6">  (ID: {{ Object.values(this.Alert._id)[0] }})</span></p>
            <button type="button" class="delete" @click="showObservationModal=false"/>
          </header>
          <section class="modal-card-body">             
            <b-table :data="is_notes_Empty() ? [] : Alert.notes" striped narrowed hoverable focusable class="mb-3" >
                <b-table-column field="date" label="Data" centered v-slot="props">                
                        {{ new Date(Object.values(props.row.date)[0]).toLocaleDateString() }}                
                </b-table-column>
                <b-table-column field="date" label="Hora"  centered v-slot="props">                
                        {{ new Date(Object.values(props.row.date)[0]).toLocaleTimeString() }}                
                </b-table-column>
                <b-table-column field="note" label="Observação"  v-slot="props" >
                    {{ props.row.note }}
                </b-table-column>
                <b-table-column field="user" label="Autor"  v-slot="props">
                    {{ props.row.user }}
                </b-table-column>
                <template #empty>
                    <div class="has-text-centered">Sem observações inseridas</div>
                </template>
            </b-table> 
           <br>
          <footer >
            <b-field label="Nova Observação" label-position="on-border">
              <b-input expanded v-model='notes' ></b-input>
              <p class="control" >
                  <b-button rounded class="is-success" @click="insertNotes()" >Inserir</b-button>
              </p>
            </b-field>  
                     
          </footer>
          </section>
        </div>
        </b-modal>
  </div>
 
</template>

<style lang="scss">
.is-observation {   
    float: right;
    margin-top: -30px;
    margin-right: 50px;
    display: inline-block;
}
#alerta_nao_classificado {
    font-size: 100%;
    color: rgb(245, 46, 11);
}

.has-text-underlined {
  border-bottom: 2px solid rgba(42, 157, 143, 0.3);
}
img {
  display: block;
}

.is-custom-size{
    font-size: 1.2vh;
}

.has-right-space {
  margin-right: 0.5vw;
}

.has-pointer-cursor {
  cursor: pointer;
}
.is-floating-left {
  float: right;
  margin-top: -30px;
  margin-right: -30px;
  display: inline-block;
}

.is-floating-right {
  float: right;
  margin-top: -30px;
  margin-right: 10px;
  display: inline-block;
}
</style>
<script>
import axios from 'axios'
import AlertCardBox from "@/components/AlertCardBox.vue";

export default {
  props: {
    Alert: Object,
  },
  data() {
    return {
        IsImageModalActive: false,
        thumb_up: this.Alert.thumb_up,  // Object.assign({},this.thumb_up),  // associando variaveis que vem do banco de dados
        thumb_down: this.Alert.thumb_down,  // Object.assign({},this.thumb_up), // a variaveis locais
        add: this.Alert.imageUrl,
        showObservationModal:false,
        notes:'',
        ip: process.env.VUE_APP_IP,
        
        }
},
  computed: {
        continuous_out_of_time: function (){  // fica verificando se estourou o tempo limite de observação
            return this.out_of_time()
        },
  },
  components: {
    AlertCardBox,
  },
  
  methods: {
    get_ip(){
      return process.env.VUE_APP_IP
    },
    get_libera_audio_epis(){  //navbar --> botão que permite liberar/bloquear audio
      if(localStorage.habilita_audio_epis==true || localStorage.habilita_audio_epis=='true'){
        return true
      }
      else{
        return false
      }
    },
    get_libera_audio_red(){  //navbar --> botão que permite liberar/bloquear audio
      if(localStorage.habilita_audio_red==true || localStorage.habilita_audio_red=='true'){
        return true
      }
      else{
        return false
      }
    },
    out_of_time(){  // alerta chegou e não atualizou a pagina ainda (<15s) (ocyan)
      if(this.get_delta_time() < 15000 && this.Alert.alerts[0].toString() != '0' && (this.thumb_up=='false'||this.thumb_up==false) && (this.thumb_down=='false'||this.thumb_down==false)  ){       
          if(this.get_libera_audio_epis()){    // variavel acessivel no navbar, inicialmente no login = true
          this.Play_audio(1);
          }
          console.log("Alerta Sonoro emitido epis")
            // ocyan pediu para tirar alerta por tempo
          return "" //Atenção, classificar alerta!"  // alertar
      }
      else if(this.get_delta_time() < 15000 && this.Alert.alerts[1].toString() != '0' &&(this.thumb_up=='false'||this.thumb_up==false) && (this.thumb_down=='false'||this.thumb_down==false)  ){       
          if(this.get_libera_audio_red()){    // variavel acessivel no navbar, inicialmente no login = true
          this.Play_audio(1);
          }
          console.log("Alerta Sonoro emitido red zone")
            // ocyan pediu para tirar alerta por tempo
          return "" //Atenção, classificar alerta!"  // alertar
      }
      else{
          return "" //Date.now().toString()  + " " + delta_timer.toString() + " " + (Date.now()-delta_timer).toString()
      }
    },
    get_delta_time(){
      return Date.now()-parseInt(this.Alert.timestamp);
    },
    company(){
      return localStorage.harpiaCompany
    },
    is_notes_Empty(){
      return this.notes.lenght > 0
    },
    insertObservation(){
      this.notes=''
      this.showObservationModal=!this.showObservationModal
    },
    insertNotes(){      
      
      axios.get('http://'+ this.get_ip() +':8085/insertNotes/'+this.notes+'/'+localStorage.harpiaUser +'/'+Object.values(this.Alert._id)[0]+'/ocyan')
        this.updateFirebase(this.thumb_up)
        this.insertObservation()
        window.location.reload()
      
    },
    Play_audio(vol){
        var audio = new Audio(require("../assets/beep-12.wav"));
        audio.volume = vol
        audio.play()
        return audio
    },
    GetLicenseKey() {
        return localStorage.harpiaPassword
    },
    update_alert_db(){  // troca o endereço da imagem no db e sua localização (no backend)
        // de acordo com thumb_up / thumb_down setados em true ou false o add no database muda
      
        return axios.get('http://' + this.get_ip() + ':8085/alerts/update/' + this.GetLicenseKey() + '/' + Object.values(this.Alert._id)[0] +"/"+ this.thumb_up+"/"+ this.thumb_down)
    },

  
    invert_thumb_up() {  
        if (this.thumb_up == false || this.thumb_up == 'false') {  // false false ou false true
            this.thumb_up = 'true'
            this.thumb_down = 'false'     // protecao pra nao gerar estado true true          
            this.update_alert_db()/* .then(()=>{ this.updateFirebase(this.get_thumb_up) */
            return false            
        } 
        else {  // true false
            this.thumb_up = 'false'
            this.update_alert_db()/* .then(()=>{ this.updateFirebase(this.get_thumb_up) */
             return true
           
        }
        
    },
    get_thumb_up() {
        return this.thumb_up
    },
    invert_thumb_down() {  
        if (this.thumb_down == false || this.thumb_down == 'false') {  // retorna o estado anterior
            this.thumb_down = 'true'       // usado para não salvar a imagem do alerta 2x
            this.thumb_up = 'false'   // protecao para nao acontecer true true nos thumbs
            this.update_alert_db()/* .then(()=>{ this.updateFirebase(this.get_thumb_up) */
            return false            
        } 
        else {
            this.thumb_down = 'false'
            this.update_alert_db()/* .then(()=>{ this.updateFirebase(this.get_thumb_up) */
            return true            
        }        
    },
    get_thumb_down() {
        return this.thumb_down
    },
    // inserir try except
    get_alert_image() {
      return 'http://' + this.get_ip() + ':8085/alerts/image/' + this.GetLicenseKey() + '/' + Object.values(this.Alert._id)[0]
    },
},
created(){
  // se tiver alerta novo play audio
  this.out_of_time();
}
}
</script>