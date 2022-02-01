<template>
    <div>
    <harpiaBar />
        <div class="columns">
          <div class="column is-2 mx-4">
              <p class="subtitle mt-4">Selecione a camera:</p>
                <div v-for="cam in cameras" :key="cam">
                        <input type="radio" id="cam" :value="cam" v-model="camSelected"/>
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


                <v-stage ref="stage" :config="stageConfig">

      <v-layer ref="layer">
        <v-image v-if="camSelected=='cam1'" @click="handleMouseClick" :config="{image: imageParameters1,scaleX: 0.75,scaleY: 0.75,}"/>
        <v-image v-if="camSelected=='cam2'" @click="handleMouseClick" :config="{image: imageParameters2,scaleX: 0.75,scaleY: 0.75,}"/>
        <v-image v-if="camSelected=='cam3'" @click="handleMouseClick" :config="{image: imageParameters3,scaleX: 0.75,scaleY: 0.75,}"/>
        <v-image v-if="camSelected=='cam4'" @click="handleMouseClick" :config="{image: imageParameters4,scaleX: 0.75,scaleY: 0.75,}"/>
        <v-image v-if="camSelected=='cam5'" @click="handleMouseClick" :config="{image: imageParameters5,scaleX: 0.75,scaleY: 0.75,}"/>
        <v-image v-if="camSelected=='cam6'" @click="handleMouseClick" :config="{image: imageParameters6,scaleX: 0.75,scaleY: 0.75,}"/>
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
      stageConfig: {
        width: '',
        height: '',
      },
      rdSelected:'',
      redzones:[],
      redzonesAtivas:[],
      cameras:["cam1","cam2","cam3","cam4","cam5","cam6",],
      camSelected:'cam1',
      image: null,
      anchors: [],
      points: [],
      close:true,
      imageParameters1: new window.Image(),
      imageParameters2: new window.Image(),
      imageParameters3: new window.Image(),
      imageParameters4: new window.Image(),
      imageParameters5: new window.Image(),
      imageParameters6: new window.Image()
    };
  },
  created() {
    this.loadingImages()
    this.loadRedZones()

  },
  watch:{
    camSelected:{
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
      let whichcam = String(1)
      this.imageParameters1.src=require('@/assets/cam'+ whichcam +".jpg")
      this.imageParameters1.onload = () => {
      this.image=this.imageParameters1
      this.stageConfig.width = 1980 ;
      this.stageConfig.height = 1080 ;
        };
      this.imageParameters2.src=require('@/assets/cam2.jpg')
      this.imageParameters2.onload = () => {
      this.stageConfig.width = 1980 ;
      this.stageConfig.height = 1080 ;
        };
      this.imageParameters3.src=require('@/assets/cam3.jpg')
      this.imageParameters3.onload = () => {
      this.stageConfig.width = 1980 ;
      this.stageConfig.height = 1080 ;
        };
      this.imageParameters4.src=require('@/assets/cam4.jpg')
      this.imageParameters4.onload = () => {
      this.stageConfig.width = 1980 ;
      this.stageConfig.height = 1080 ;
        };
      this.imageParameters5.src=require('@/assets/cam5.jpg')
      this.imageParameters5.onload = () => {
      this.stageConfig.width = 1980 ;
      this.stageConfig.height = 1080 ;
        };
      this.imageParameters6.src=require('@/assets/cam6.jpg')
      this.imageParameters6.onload = () => {
      this.stageConfig.width = 1980 ;
      this.stageConfig.height = 1080 ;
        };

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
      axios.get('loaddots/'+ this.camSelected).then((resp)=>{
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
      axios.get('loaddots_ativos/'+ this.camSelected ).then((resp)=>{
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
    save(){
    // precisa ser substituido por algo sem buefy --> pensei num componente
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
          x_y.push(', largura: '+this.stageConfig.width)
          x_y.push(', altura: '+ this.stageConfig.height+', pontos: ')
          this.points.forEach(p => {
            x_y.push(p)
            x_y.push(',')
          });

          // cria o blob com a resolucao da imagem nos dois primeiros elementos do array
          var blob = new Blob(x_y, {type: "text/plain;charset=utf-8"});
          var myformData = new FormData();
          myformData.append("txt", blob, "1.txt")
          axios.post('http://' + this.get_ip() + ':8085/savedots/'+ this.camSelected + "/" + this.key(), myformData, {
            headers: {'Content-Type': 'text/plain; charset=UTF-8'}}).then(()=>this.loadRedZones())
            }
          })
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
          axios.post('http://' + this.get_ip() + ':8085/deldots/'+ this.camSelected + "/" + this.key()+ "/" + rz.nome).then((r)=>{
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
          axios.post('http://' + this.get_ip() + ':8085/savedots/'+ this.camSelected + "-ativas/" + this.key(), myformData, {
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
          axios.post('http://' + this.get_ip() + ':8085/deldots/'+ this.camSelected +"-ativas/" + this.key()+ "/" + rz.nome).then((r)=>{
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