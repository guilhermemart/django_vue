<template>
  <div>
  <div class="box has-background-white">
    <div>
      <button class=" button is-observation is-rounded is-small is-info">O</button>
      <button class=" button is-floating-right is-rounded is-small is-success">L</button>
      <button class=" button is-floating-left is-rounded is-small is-danger">D</button>
      <div class="columns">
        <div class="column is-4">

        </div>
        <div class="column is-3">
          <p class="dates mb-3">{{new Date(Alert.timestamp).toLocaleDateString("en-US")}}</p>

          <p class="dates">{{new Date(Alert.timestamp).toLocaleTimeString("en-US")}}</p>

        </div>

        <div class="column is-5">
          <figure class="image">
            <!--img src "imagem aqui" -->
            <img :src="Alert.get_thumbnail">
          </figure>
        </div>


      
      </div>  
    </div>
  
  </div>


  <div class="card" v-if="false">
  <nav class="breadcrumb is-right" aria-label="breadcrumbs">
    <ul>
      <li v-if="thumb_up"><button class="button" @click="invert_thumb_up()" >thumbup_on </button></li>
      <li v-else><button class="button" @click="invert_thumb_up()">thumbup_off </button></li>
      <li v-if="thumb_down"><button class="button" @click="invert_thumb_down()" >thumbdown_on </button></li>
      <li v-else><button class="button" @click="invert_thumb_down()">thumbdown_off </button></li>
      <li><button class="button" @click="insert_notes()">notes {{modal}}</button></li>
    </ul>
  </nav>
    <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image">
                  <!--img src "imagem aqui" -->
                  <img :src="Alert.get_thumbnail">
                </figure>
                Alert id: {{Alert.id}}
              </div>
            <div class="media-content is-right">
              <!-- Obs: os ':' servem para passar variavel, sem eles passa string --> 
              <alert_card_box v-if="Alert.data_1" :label="Alert.label_1" :data="Alert.data_1" />
              <alert_card_box v-if="Alert.data_2" :label="Alert.label_2" :data="Alert.data_2" />
              <alert_card_box v-if="Alert.data_3" :label="Alert.label_3" :data="Alert.data_3" />
              <alert_card_box v-if="Alert.data_4" :label="Alert.label_4" :data="Alert.data_4" />
            </div>
<router-link v-bind:to="Alert.get_absolute_url" class="button is-dark mt-4">View details</router-link>
        </div>
    </div>

  </div>
  <!-- card antigo
    <div class="has-text-right mb-4">
      <button v-if= "get_thumb_up() == 'true'" size="is-small" icon-right="thumb-up" class="is-floating-right" rounded inverted type= 'is-success' @click="invert_thumb_up()" />
      <button v-else size="is-small" icon-right="thumb-up" class="is-floating-right"  rounded inverted  @click="invert_thumb_up()"/>
      <button v-if= "get_thumb_down() == 'true'" size="is-small" icon-right="thumb-down" class="is-floating-left" rounded inverted  type= 'is-danger' @click="invert_thumb_down()"/>
      <button v-else size="is-small" icon-right="thumb-down" class="is-floating-left"  rounded inverted  @click="invert_thumb_down()" />
      <button size="is-small" icon-right="message" class="is-observation" rounded inverted
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
        <alert_card_box :Label="'Data'" :Data="new Date(Object.values(Alert.datetime)[0]).toLocaleDateString('pt-BR')"/>
        <alert_card_box :Label="'Hora'" :Data="new Date(Object.values(Alert.datetime)[0]).toLocaleTimeString('pt-BR')"/>

        
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
  </div>-->
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
.dates{
    padding: .01vh .10vw .01vh;
    border: .5px solid rgb(82, 82, 82);
    border-radius: 8px;
    margin-top: 1vh;
    font-size: 2vh;
  
}
</style>
<script>
import axios from 'axios'
import alert_card_box from "@/components/alert_card_box.vue";

export default {
  props: {
    Alert: Object,
  },
  data() {
    return {
        thumb_up: false,
        thumb_down: true,
        modal: true,
        notes: "0"
        }
  },
  components: {
    alert_card_box,
  },
  mounted(){
        this.preencher_card()
  },
  methods: {
    invert_thumb_up(){
        this.thumb_up = !this.thumb_up
        if(this.thumb_up){
            this.thumb_down = false
        }
        const formData = {
                identificador: this.Alert.identificador,
                thumb_up: this.thumb_up,
                thumb_down: this.thumb_down
                // to do notes:this.notes
            }

            axios
                .post("/api/v1/update_alert_by_identificador/", formData)
                .then(response => {
                })
                .catch(error => {
                    console.log(error)
                })
        return this.thumb_up
    },
    invert_thumb_down(){
        this.thumb_down = !this.thumb_down
        if(this.thumb_down){
            this.thumb_up = false
        }
        const formData = {
                identificador: this.Alert.identificador,
                thumb_up: this.thumb_up,
                thumb_down: this.thumb_down
                // to do notes:this.notes
            }

            axios
                .post("/api/v1/update_alert_by_identificador/", formData)
                .then(response => {
                })
                .catch(error => {
                    console.log(error)
                })
        return this.thumb_down
    },
    insert_notes(){
        this.modal = !this.modal
    },
    preencher_card(){
        this.thumb_up=this.Alert.thumb_up
        this.thumb_down=this.Alert.thumb_down
    }
  },
  computed: {

  },

}
</script>