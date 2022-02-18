<template>
    <div>
    <harpiaBar />
        <div class="columns">
          <div class="column is-2 mx-4">
              <p class="subtitle mt-4">Selecione a camera:</p>
                <div v-for="cam in cameras" :key="cam">
                        <input type="radio" id="cam" :value="cam" v-model="cam_selected"/>
                         <label for="cam">{{cam}}</label>
                </div>
              <button class="is-danger my-2" icon-left="broom"  expanded outlined @click="clear">Limpar</button>
              <button class="is-warning mb-2" icon-left="undo" :disabled='this.points.length<2' expanded outlined @click="undo">Desfazer</button>
              <button class="is-success mb-2"  icon-left="content-save" :disabled='this.points.length<6' expanded outlined @click="save">Salvar</button>
            <dropdown expanded  v-model="rdSelected" aria-role="list">
              <template #trigger>
              <button class="is-dark mb-2"  icon-left="upload" :disabled='redzones.length<1' expanded outlined >Carregar</button>
              </template>
              <dropdown-item v-for="rd in redzones" :key="rd.nome" :value="rd" aria-role="listitem" class="columns">
                  <div class="column"><button @click="deleteRZ(rd)" icon-left="delete" size='is-large' class="is-danger" inverted ></button>
                  </div><div class="column my-4">{{rd.nome.toUpperCase()}}</div>
              </dropdown-item>
            </dropdown>
            <button class="is-info mb-4"  icon-left="play" :disabled='this.points.length<6' expanded outlined @click="enableRZ(rdSelected)">Ativar RedZone</button>

            <div class="card">
              <p class="title is-size-4">Red Zones Ativas:</p>
              <div v-if="redzonesAtivas.length">
              <ul class="is-size-4 mx-2 my-2" v-for="rz in redzonesAtivas" :key='rz.nome'><hr> <button class=" mb-2 is-danger" outlined rounded   @click="disabledRZ(rz)">Desabilitar</button> <b class="my-4">{{rz.nome}}</b> </ul>
              </div>
              <div v-else class="is-size-4 card"> <p><i>Sem redzones ativas no momento.</i></p></div>
            </div>


            </div>
            <div class=" cams column is-10 mt-4 " >


                <v-stage ref="stage" :config="stageConfig[cam_selected]">

      <v-layer ref="layer">
        <v-image @click="handleMouseClick" :config="{image: imageParameters[cam_selected],scaleX: 0.75,scaleY: 0.75,}"/>
        <v-line
          :config="{
            fill:'hsla(0, 100%, 50%, 0.5)',
            points: points,
            tension: 0,
            closed: close,
            stroke: 'black'}"/>

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
      stageConfig: [],
      rdSelected:'',
      redzones:[],
      redzonesAtivas:[],
      cameras:["cam1","cam2","cam3","cam4","cam5","cam6",],
      cam_selected: 1,
      anchors: [],
      points: [],
      close:true,
      num_cameras: 6,
      imageParameters: [],
    };
  },
  created() {
    this.loadingImages()
    this.loadRedZones()

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
    /*user() {
      return localStorage.harpiaUser
      },
    key() {
      return localStorage.harpiaPassword
      },*/
    loadingImages(){
      let base_path= "@/assets/red_zones_base_img/cam"
      which_camera = 0
      while (wich_camera < num_cameras){
      this.imageParameters[wich_camera].src=require(base_path + wich_camera.toString() +".jpg")
      this.imageParameters[wich_camera].onload = () => {
      this.stageConfig[which_camera]={
        width : this.imageParameters[wich_camera].naturalWidth ,
        height : this.imageParameters[wich_camera].naturalHeight
        }}
      wich_camera +=1
      }},
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
    },
    updatePoly(event) {
      const mousePos = this.$refs.stage.getNode().getPointerPosition();
      const x = mousePos.x;
      const y = mousePos.y;
      const id = event.target.id();
      const item = this.anchors.find((i) => i.id === id);
      const index = this.anchors.indexOf(item);
      this.points[index * 2] = x;
      this.points[index * 2 + 1] = y;
    },
    loadRedZones(){
      this.redzones=[]
      axios.get('loaddots/'+ this.cam_selected).then((resp)=>{
        let rzCadastradas = resp.data.conteudo.split('\n')
        console.log(resp.data.conteudo)
        rzCadastradas.pop()
        rzCadastradas.forEach(element => {

          let pontos=element.split(',').splice(3,element.split(',').length-1)
          pontos[0]=pontos[0].replace(' pontos: ',"")
          pontos.pop()
          let r ={}
          r.nome=element.split(',')[0].replace('nome: ',''),
          r.largura=element.split(',')[1].replace('largura: ',''),
          r.altura=element.split(',')[2].replace('altura: ',''),
          r.pontos=pontos.map(Number)
          this.redzones.push(r)
        });
      })



      this.redzonesAtivas=[]
      axios.get('loaddots_ativos/'+ this.cam_selected ).then((resp)=>{
        let rzAtivas = resp.data.conteudo.split('\n')
        rzAtivas.pop()
        rzAtivas.forEach(element => {

          let pontos=element.split(',').splice(3,element.split(',').length-1)
          pontos[0]=pontos[0].replace(' pontos: ',"")
          pontos.pop()
          let r ={}
          r.nome=element.split(',')[0].replace('nome: ',''),
          r.largura=element.split(',')[1].replace('largura: ',''),
          r.altura=element.split(',')[2].replace('altura: ',''),
          r.pontos=pontos.map(Number)
          this.redzonesAtivas.push(r)
        });
      }).catch(error=>{
      console.log(error)
      })
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
            nome: (new Date()).toString(),
            largura: this.stageConfig[cam_selected].width,
            pontos: x_y}
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
    //old
    /* precisa ser substituido por algo sem buefy --> pensei num componente
      this.$buefy.dialog.prompt({
        message: `Nome desta redzone:`,
        type:'is-success',
        size:'is-large',
        inputAttrs: {
          placeholder: 'Nome da redzone',
          maxlength: 20
        },
        confirmTest:'Salvar',
        trapFocus: true,
        onConfirm: (rdName) => {
          //var FileSaver = require('file-saver');
          var x_y=[]
          x_y.push('nome: '+rdName)
          x_y.push(', largura: '+this.stageConfig[cam_selected].width)
          x_y.push(', altura: '+ this.stageConfig[cam_selected].height+', pontos: ')
          this.points.forEach(p => {
            x_y.push(p)
            x_y.push(',')
          });

          // cria o blob com a resolucao da imagem nos dois primeiros elementos do array
          var blob = new Blob(x_y, {type: "text/plain;charset=utf-8"});
          var myformData = new FormData();
          myformData.append("txt", blob, "1.txt")
          axios.post('http://' + this.get_ip() + ':8085/savedots/'+ this.cam_selected + "/" + this.key(), myformData, {
            headers: {'Content-Type': 'text/plain; charset=UTF-8'}}).then(()=>this.loadRedZones())
            }
          })*/
    },
    clear() {
      this.points = [];
      this.anchors = [];
      this.loadRedZones()
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
            this.loadRedZones()
          })
        }
      })
    },
    enableRZ(rz){
      alert(rz.nome)
      var x_y=[]
          x_y.push('nome: '+rz.nome)
          x_y.push(', largura: '+rz.largura)
          x_y.push(', altura: '+ rz.altura+', pontos: ')
          rz.pontos.forEach(p => {
            x_y.push(p)
            x_y.push(',')
          });

          // cria o blob com a resolucao da imagem nos dois primeiros elementos do array
          var blob = new Blob(x_y, {type: "text/plain;charset=utf-8"});
          var myformData = new FormData();
          myformData.append("txt", blob, "1.txt")
          axios.post('http://' + this.get_ip() + ':8085/savedots/'+ this.cam_selected + "-ativas/" + this.key(), myformData, {
            headers: {'Content-Type': 'text/plain; charset=UTF-8'}}).then(()=>this.loadRedZones())


    },
    disabledRZ(rz){
       this.$buefy.dialog.confirm({
        message: `Deseja desabilitar a redzone `+rz.nome+'?',
        type:'is-danger',
        size:'is-large',
        confirmText:'SIM',
        cancelText:'Não',
        trapFocus: true,
        onConfirm: () => {
          //codigo para excluir uma redzone ainda em construção.
          axios.post('http://' + this.get_ip() + ':8085/deldots/'+ this.cam_selected +"-ativas/" + this.key()+ "/" + rz.nome).then((r)=>{
            console.log(r)
            this.loadRedZones()
          })
        }
      })

    }

}
}
//bloquear a possibilidade de nomes duplicados para as redzones

</script>