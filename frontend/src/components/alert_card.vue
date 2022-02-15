<template>
  <div>
  <div class="box has-background-white">
    <div class="is-floating-left">
      <button class=" button mx-1 is-rounded is-small is-primary">O</button>
      <button class=" button mx-1 is-rounded is-small is-success">L</button>
      <button class=" button mx-1 is-rounded is-small is-danger">D</button>
    </div>
      <div class="columns column">
        <div class="column is-3 mt-4">    
            <div class=" has-text-left">
              <div class="container has-text-underlined">
                <icon  class="ml-2" icon="hard-hat" type="is-primary"></icon>
                <span  class="is-size-6 has-text-weight-bold has-text-primary">{{ Alert.quantidade }} EPI</span>
              </div>

              <div class="container has-text-underlined">
                <icon class="ml-2" icon="exclamation-thick" type="is-primary"></icon>
                <span class="is-size-6 has-text-weight-bold has-text-primary">{{ Alert.quantidade }} Red Zone</span>
              </div>

              <span class="has-text-grey-light is-custom-size">ID: {{ Alert.identificador }}</span>
            </div>
          </div>

        <div class="column is-3 ">
          <p class="dates mb-3"><p>Date:</p>{{new Date(Alert.timestamp).toLocaleDateString("en-US")}}</p>
          <p class="dates"> <p>Time:</p>{{new Date(Alert.timestamp).toLocaleTimeString("en-US")}}</p>

        </div>

        <div class="column is-5 thumb ">
          <figure class="image">
            <!--img src "imagem aqui" -->
            <img :src="Alert.get_thumbnail " class="has-pointer-cursor" >
          </figure>
        </div>


      
      </div>  
    </div>
  
  </div>

</template>

<style lang="scss">
.thumb{
position: relative;
margin-left: 25%;
}
.is-observation {   
    float: right;
    margin-top: -35px;
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


.is-custom-size{
    font-size: 1.2vh;
}


.has-pointer-cursor {
  cursor: pointer;
}
.is-floating-left {
  float: right;
  margin-top: -39px;
  margin-right: -30px;
  display: inline-block;
}

.is-floating-right {
  float: right;
  margin-top: -35px;
  margin-right: 11px;
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