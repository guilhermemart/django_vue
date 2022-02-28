<template>
    <div>
    <harpiaBar />
        <div class="columns">
          <div class="column is-2 mx-4">
              <p class="subtitle mt-4">Selecione a camera:</p>
                <div v-for="cam in stageConfig" :key="cam.name">
                        <input type="radio" id="cam.name" :value="cam.name" v-model="cam_selected"/>
                         <label for="cam"> cam{{(cam.name+1)}}</label>
                </div>
              <button class="is-danger my-2" icon-left="broom"  expanded outlined @click="clear">Limpar</button>
              <button class="is-warning mb-2" icon-left="undo" :disabled='this.points.length<2' expanded outlined @click="undo">Desfazer</button>
              <button class="is-success mb-2"  icon-left="content-save" :disabled='this.points.length<6' expanded outlined @click="save">Salvar</button>
            <div class="dropdown is-hoverable">
              <div class="dropdown-trigger">
                <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
                  <span>Carregar</span>
                  <span class="icon is-small">
                    <i class="fas fa-angle-down" aria-hidden="true"></i>
                  </span>
                </button>
              </div>
              <div class="dropdown-menu" id="dropdown-menu" role="menu">
                <div class="dropdown-content">
                  <a v-for="rd in redzones" :key="rd.name" :value="rd" aria-role="listitem" class="columns">
                  <div class="column"><button @click="deleteRZ(rd)" icon-left="delete" size='is-large' class="is-danger" inverted >delete icon</button></div>
                  <div class="column my-4">{{rd.name.toUpperCase()}}</div>
                  </a>
                </div>
              </div>
            </div>

            <button class="is-info mb-4"  icon-left="play" :disabled='this.points.length<6' expanded outlined @click="enableRZ(rdSelected)">Ativar RedZone</button>
            <div class="card">
              <p class="title is-size-4">Red Zones Ativas:</p>
              <div v-if="red_zones_ativas.length">
              <ul class="is-size-4 mx-2 my-2" v-for="rz in red_zones_ativas" :key='rz.name'><hr> <button class=" mb-2 is-danger" outlined rounded   @click="disabledRZ(rz)">Desabilitar </button> <b class="my-4">{{rz.name}}</b> </ul>
              </div>
              <div v-else class="is-size-4 card"> <p><i>Sem redzones ativas no momento.</i></p></div>
            </div>
            </div>
            <div class=" cams column is-10 mt-4 " >

<!--v-stage e v-layer são classes do vue-konva -->
                <v-stage ref="stage" :config="stageConfig[cam_selected]">

      <v-layer ref="layer">
        <v-image @click="handleMouseClick" :config="{image: imageParameters[cam_selected],scaleX: scale,scaleY: scale,}"/>
        <v-line
          :config="{
            fill:'hsla(0, 100%, 50%, 0.5)',
            points: points,
            tension: 0,
            closed: close,
            stroke: 'black'}"/>
        <!-- circulinho vermelho que aparece qdo clicamos -->
        <v-circle
          @dragmove="updatePoly"
          v-for="item in anchors"
          :key="item.id"
          :config="{
            id: item.id,
            x: item.x,
            y: item.y,
            radius: 4,
            fill: 'red',
            stroke: 'black',
            draggable: true,
          }"
        />
      </v-layer>
    </v-stage>
            </div>
        </div>
    </div>
</template>
<style lang="scss">

</style>

<script>
import axios from 'axios'
import harpiaBar from '@/components/harpiaBar.vue'
//const width = window.innerWidth;
//const height = window.innerHeight;

export default {
    name:'Redzones',
    components: {
    harpiaBar,
    },
  data() {
    return {
      scale:0.5,  // a escala das imagens deve ser fixa pois os pontos são pegos em relação a posição do mouse
      stageConfig: [],  // array onde as caracteristicas das imagens são armazenadas
      rdSelected:'',  // variavel watchada para mostrar o poligono qdo clica na rz
      redzones:[],  // array de redzones
      red_zones_ativas:[],  //array de redzones ativas
      cam_selected: 0,  // camera em operação
      anchors: [],
      points: [],
      close:true,
      num_cameras: 6,  // selecionar o numero de cameras para parametrizar o looping
      imageParameters: [],  // array para armazenar as imagens base
    };
  },
  created() {
    this.loadingImages()  // le as imagens base onde os pontos serão desenhados
    this.load_red_zones()
  },
  watch:{
    cam_selected:{
      handler(){
        this.clear()
      }
    },
    rdSelected:{
      handler(){
        this.clear()
        this.points=this.rdSelected.pontos
      }
    }
  },methods: {
    get_ip(){
      return process.env.VUE_APP_IP
      },

    async loadingImages(){
    this.$store.commit('setIsLoading', true)
      let which_camera = 0
      while (which_camera < this.num_cameras){
        this.imageParameters.push(new window.Image())
        this.imageParameters[which_camera].src=require('@/assets/red_zones_base_img/cam'+which_camera.toString()+'.jpg')
        this.stageConfig.push({
            name : which_camera,
            width : this.imageParameters[which_camera].naturalWidth,
            height : this.imageParameters[which_camera].naturalHeight
        })
        which_camera +=1
      }
      this.$store.commit('setIsLoading', false)
    },
    // precisa colocar isso no watch
    load_red_zones(){
        this.redzones=[]
        this.red_zones_ativas=[]
        let rz_cadastradas = []
        /* campos minimos esperados de red zones
        name:
        width:
        heigth:
        enabled:
        dots: [] */
        // feito o get pro django retorna um objeto javascript --> magia do rest_api
        axios.get('api/v1/load_rz/'+ this.cam_selected).then((rzones)=>{
        // todas as redzones da camera atual retornarão na forma de uma lista de objetos
            for(let i=0; i < rzones.data.length; i = i + 1){
                this.redzones.push(rzones.data[i])
                this.redzones[i].dots = this.redzones[i].dots.map(Number)
                if (this.redzones[i].enabled == true){
                    this.red_zones_ativas.push(this.redzones[i])
                }
            }
        }).catch((error)=>{
            console.log(error)
        })
    },

    handleMouseClick() {
      const mousePos = this.$refs.stage.getNode().getPointerPosition();
      const x = mousePos.x;
      const y = mousePos.y;
      this.anchors.push({
        id: Math.round(Math.random() * 10000).toString(),
        x: x,
        y: y,
      });
      this.points.push(x);
      this.points.push(y);
      console.log(x)
    },
    updatePoly(event) {
      const mousePos = this.$refs.stage.getNode().getPointerPosition();
      const x = mousePos.x;
      const y = mousePos.y;
      const id = event.target.id();
      const item = this.anchors.find((i) => i.id === id);
      const index = this.anchors.indexOf(item);
      //o que isso faz?
      this.points[index * 2] = x;
      this.points[index * 2 + 1] = y;
    },

    async save(){
        var x_y=[]
        //x_y.push('nome: '+(new Date()).toString())
        //x_y.push(', largura: '+this.stageConfig[cam_selected].width)
        //x_y.push(', altura: '+ this.stageConfig[cam_selected].height+', pontos: ')
        this.points.forEach(p => {
            x_y.push(p)
        });
        var red_zone_output = {
            cam: this.cam_selected,
            name: "cam" + this.cam_selected.toString() + "_" + (new Date().getTime()).toString(),
            width: this.stageConfig[this.cam_selected].width,
            height: this.stageConfig[this.cam_selected].heigth,
            dots: x_y}
        this.$store.commit('setIsLoading', true)
      await axios
        .post('/api/v1/save_red_zone/', JSON.stringify(red_zone_output), {headers:{'Content-Type': 'application/json'}})
        .then(response => {
          red_zone_output = JSON.parse(response.data)
          console.log(red_zone_output)
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    },
    clear() {
      this.points = [];
      this.anchors = [];
      this.load_red_zones()
    },
    undo() {
      this.points.pop();
      this.points.pop();
      this.anchors.pop();
    },
    deleteRZ(rz){
       this.$buefy.dialog.confirm({
        message: `Deseja excluir a redzone: `+rz.nome+'?',
        type:'is-success',
        size:'is-large',
        confirmTest:'Confirmar',
        trapFocus: true,
        onConfirm: () => {
          //codigo para excluir uma redzone ainda em construção.
          axios.post('http://' + this.get_ip() + ':8085/deldots/'+ this.cam_selected + "/" + this.key()+ "/" + rz.nome).then((r)=>{
            console.log(r)
            this.load_red_zones()
          })
        }
      })
    },
    enableRZ(rz){
      alert(rz.nome)
          axios.post('api/v1/update_red_zone/'+ rz.name,JSON.stringify({is_active: true}), {headers:{'Content-Type': 'application/json'}}).then(()=>this.load_red_zones())
    },

    disabledRZ(rz){
          axios.post('api/v1/update_red_zone/'+ rz.name,JSON.stringify({is_active: false}), {headers:{'Content-Type': 'application/json'}}).then(()=>this.load_red_zones())
    }

}
}
//bloquear a possibilidade de nomes duplicados para as redzones

</script>