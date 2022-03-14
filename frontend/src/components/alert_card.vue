<template>
  <div>
    <div class="box has-background-white mx-1" :class="thumb_up?'boxUp':thumb_down?'boxDown':'box'">
      <div class="is-floating-left">
        <button class=" button mx-1 is-rounded is-small is-dark is-inverted is-focused" @click="commentModal=!commentModal" >
          <span class="icon ">
            <i class="far fa-comment-alt fa-lg" />
          </span>
        </button>
        <button v-if="thumb_up" class=" button mx-1 is-rounded is-small is-dark is-inverted is-focused is-success" @click="invert_thumb_up" >
          <span class="icon ">
            <i class="far fa-thumbs-up fa-lg" />
          </span>
        </button>
        <button v-else class=" button mx-1 is-rounded is-small is-dark is-inverted is-focused" @click="invert_thumb_up" >
          <span class="icon ">
            <i class="far fa-thumbs-up fa-lg" />
          </span>
        </button>
        <button v-if="thumb_down" class=" button mx-1 is-rounded is-small  is-inverted is-focused is-danger" @click="invert_thumb_down" >
          <span class="icon ">
            <i class="far fa-thumbs-down fa-lg" />
          </span>
        </button>
        <button v-else class=" button mx-1 is-rounded is-small is-dark is-inverted is-focused"  @click="invert_thumb_down">
          <span class="icon ">
            <i class="far fa-thumbs-down fa-lg" />
          </span>
        </button>
      </div>
            
      <div class="columns column mt-1">
        <div class="column is-4 mt-4">    
            <div class=" has-text-left">
              <div class="container has-text-underlined mb-4">
                <icon  class="ml-2 " icon="hard-hat" type="is-primary"></icon>
                <span  class="is-size-5 has-text-weight-bold has-text-primary">{{ Alert.quantidade }} EPI</span>
              </div>
              <div class="container has-text-underlined">
                <icon class="ml-2" icon="exclamation-thick" type="is-primary"></icon>
                <span class="is-size-5 has-text-weight-bold has-text-primary">{{ Alert.quantidade }} Red Zone</span>
              </div>
              <span class="has-text-grey-light is-custom-size">ID: {{ Alert.identificador }}</span>
            </div>
        </div>

        <div class="column is-4 ">
          <p class="dates mb-3"><p>Date:</p>{{new Date(Alert.timestamp).toLocaleDateString("en-US")}}</p>
          <p class="dates"> <p>Time:</p>{{new Date(Alert.timestamp).toLocaleTimeString("en-US")}}</p>
        </div>

        <div class="column is-4">          
          <figure class="image">
            <!--img src "imagem aqui" -->
            <img :src="Alert.get_thumbnail " class="has-pointer-cursor" @click="imageModal=!imageModal">
          </figure>
        </div>

    
        <div class="modal" @click="imageModal=!imageModal" :class="{'is-active': imageModal}">
          <div class="modal-background"> </div>
          <!--
          Para fazer depois:
          Aumentar o modal, talvez a solução seja o  https://postare.github.io/bulma-modal-fx/ -->
          <div class="modal-content fullImage">
            <p class="image is-16by9 ">
              <img :src="Alert.get_image" alt="">
            </p>
          </div>      
        </div>

        <div class="modal"  :class="{'is-active': commentModal}">
            
          <div class="modal-background"> </div>
          <!--
          Para fazer depois:
          Aumentar o modal, talvez a solução seja o  https://postare.github.io/bulma-modal-fx/ -->
          <div class="modal-content">
            <header class="modal-card-head">
            <p class="modal-card-title">Information </p>
            <button type="button" class="delete" @click="commentModal=false" />
          </header>
           <section class="modal-card-body">             
           
            <table :data="Alert" class="mb-3 table  is-bordered is-striped is-hoverable is-fullwidth" v-if="comments.length" >
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Hour</th>
                  <th>Notes</th>
                  <th>User</th>
                </tr>
              </thead>
              <tbody v-for="comment in comments" :key="comment">
                <tr>
                  <!-- <th>{{new Date(JSON.parse(comment).timestamp).toLocaleDateString('en-US')}}</th>
                  <th>{{new Date(JSON.parse(comment).timestamp).toLocaleTimeString('en-US')}}</th>
                  <th> {{JSON.parse(comment).comment}}</th>                  -->
                  <th>{{comment}}</th> 
                           
                </tr>
               
              </tbody>
        
              
            </table>
            <p v-else class="has-text-danger is-size-4">This alert has no comments entered.</p> 
           <br>
           <hr>
          <footer>
            <div class="field has-addons">
              <div class="control is-expanded">
               <input class="input is-rounded" v-model="note.comment" type="text" placeholder="Insert comment">
              </div>
              <div class="control">
                <button class="button is-info is-rounded" :disabled='note.comment==""' @click="insert_notes()">
               Save
                </button>
              </div>
            </div> 
                     
          </footer>
          </section>
          </div>      
        </div>
        

        
      </div>  
    </div>
    
  </div>

</template>

<style lang="scss">

.boxDown{
  border-color: red;
  border-style: solid;
  border-width: 0.05vh;
}
.boxUp{
  border-color: green;
  border-style: solid;
  border-width: 0.05vh;
}
.table{
  overflow: auto;
}
.fullImage{
  
      display: block; 
      min-width: 160vh;
      height: auto;
}

#alerta_nao_classificado {
    font-size: 100%;
    color: rgb(245, 46, 11);
}

.has-text-underlined {
  border-bottom: 2px solid rgba(42, 157, 143, 0.3);
}


.is-custom-size{
    font-size: 1.2vh;
}


.has-pointer-cursor {
  cursor: pointer;
}
.is-floating-left {
  float: right;
  margin-top: -35px;
  margin-right: -30px;
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
        thumb_down: false,
        modal: true,
        note:{comment:'',timestamp:'',user:localStorage.getItem('harpiaUser')},
        local_audio_enable: true,
        imageModal:false,
        commentModal:false,
        comments:''
        
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
        if (this.thumb_up == true){
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
        if(this.thumb_down==true){
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
      this.note.timestamp= new Date().getTime()
      let anotacao =JSON.stringify(this.note)
      console.log(anotacao)
      const formData = {
                identificador: this.Alert.identificador,
                thumb_up: this.thumb_up,
                thumb_down: this.thumb_down,
                anotacoes: JSON.stringify(this.note)
            }
            axios
                .post("/api/v1/update_alert_by_identificador/", formData)
                .then(response => {
                  console.log(response)
                  alert('foi')
                  this.commentModal=false
                  this.note.comment=''
                })
                .catch(error => {
                    console.log(error)
                })
  
      


    },
    preencher_card(){
        this.thumb_up=this.Alert.thumb_up
        this.thumb_down=this.Alert.thumb_down
    },
    get_delta_time(){
      return Date.now()-parseInt(this.Alert.timestamp);
    },
    out_of_time(){  // alerta chegou e não atualizou o thumb ainda
      if (this.$store.state.audio.has_delay == true){
      if(this.get_delta_time()>300000 && (this.thumb_up=='false') && (this.thumb_down=='false') && (this.local_audio_enable == true)){
          this.Play_audio(1);
          if(this.$store.state.audio.is_recorrente == false) {
              this.local_audio_enable = false  //caso tenha atraso e nao for recorrente esse if desabilita até dar reload na pagina
          }
          return "Atenção, classificar alerta!"  // alertar
      }
      else{
          return ""
      }}
    },
    play_audio(vol){
        if(this.$store.state.audio.is_on==true){
            var audio = new Audio(require("../assets/beep-12.wav"))
            audio.volume = vol
            audio.play()
        }
    },
    reading_notes(){
      this.comments= this.Alert.anotacoes.split("}{")
    }    
  },
  created() {
    this.reading_notes() //carregar as anotações
  },
  
  computed: {
        continuous_out_of_time: function (){  // fica verificando se estourou o tempo limite de observação
            return this.out_of_time()
        },
  },}

</script>