<template>
    <div id="main-div" class="overlay">
        <harpiaBar/>

        <!-- Div com as tabs.
         Função tabSwitcher troca o conteúdo -->

        <div class="tabs is-centered is-toggle mt-1 is-small">
          <ul>
            <li class="is-active mr-4" @click="tabSwitcher('1')">
              <a id="tabs">
                <span>Area A</span>
              </a>
            </li>
            <li class="mr-4" @click="tabSwitcher('2')">
              <a id="tabs">
                <span>Area B</span>
              </a>
            </li>
            <li @click="tabSwitcher('3')">
              <a id="tabs">
                <span>Area C</span>
              </a>
            </li>
          </ul>
        </div>

        <!-- Slider que troca o posicioamento das cameras da 'Area B' -->

        <div id="switch" v-if="group==='2'">
            <div class="slider-text">
                <font-awesome-icon icon="fa-regular fa-up-down" />
                <i class="fa-regular fa-up-down"></i>
                V -- H
            </div>
            <label class="switch">
                <input id="orientation" type="checkbox" @click="changeOrientation()">
                <span class="slider round"></span>
            </label>
        </div>

        <!-- Conteúdo das tabs
        is-multiline permite que o conteúdo vá para outra linha automaticamente,
        is-gapless n deixa espaço entre as imagens (entre elas mesmas),
        is-half faz que a coluna ocupe metade do tamanho horizontal (e só suporta 2 is-half por linha)
        ml-3 / mr-3 é um offset das bordas da página -->

        <div id="tab-content" class="columns">
            <div id="camGroupA" v-if="group==='1'" class="columns is-multiline is-gapless">
                <div class="column is-half">
                    <img id="camA1" :src="cameraA1" width="980" alt="camera 1"/>
                </div>
                <div class="column is-half">
                    <img id="camA2" src="@/assets/valaris2.jpg" width="980" alt="camera 2"/>
                </div>
                <div class="column is-half ">
                    <img id="camA3" src="@/assets/valaris3.jpg" width="980" alt="camera 3"/>
                </div>
                <div class="column is-half">
                    <img id="camA4" :src="cameraA4" width="980" alt="camera 4"/>
                </div>
            </div>

            <div id="camGroupB" v-if="group==='2'" class="columns is-multiline">
                <div id="B1" class="column is-half is-offset-3">
                    <img id="camB1" src="@/assets/valaris1.jpg" width="980" alt="camera 5"/>
                </div>
                <div id="B2" class="column is-half is-offset-3">
                    <img id="camB2" src="@/assets/valaris3.jpg" width="980" alt="camera 6"/>
                </div>
            </div>

            <div id="camGroupC" v-if="group==='3'" class="columns is-multiline is-gapless">
                <div class="column is-half">
                    <img id="camC1" src="@/assets/red_zones_base_img/cam1.jpg" width="980" alt="camera 7"/>
                </div>
                <div class="column is-half">
                    <img id="camC2" src="@/assets/valaris3.jpg" width="980" alt="camera 8"/>
                </div>
                <div class="column is-half">
                    <img id="camC3" src="@/assets/valaris1.jpg" width="980" alt="camera 9"/>
                </div>
                <div class="column is-half">
                    <img id="camC4" src="@/assets/valaris4.jpg" width="980" alt="camera 10"/>
                </div>
            </div>
        </div>

    </div>
</template>

<style>
#main-div {
    background-color: hsl(200, 5%, 5%);
    width: 100%;
    height: 100%;
}

#tabs {
    width: 8em;
    height: 1.8em;
    background: hsl(205, 90%, 50%);
    border-radius: 24px;
    transition: .3s;
}

.is-active {
    transform: scale(1.1);
    font-size: 16px;
}

.slider-text {
  color: white;
  position: absolute;
  font-size: 10px;
  right: 12.4vw;;
  top: 8em;
}

.switch {
  position: absolute;
  width: 42px;
  height: 14px;
  right: 12vw;
  top: 4em;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: dimgray;
  -webkit-transition: .3s;
  transition: .3s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 10px;
  width: 10px;
  left: 3px;
  bottom: 2px;
  background-color: white;
  -webkit-transition: .2s;
  transition: .2s;
}

input:checked + .slider {
  background-color: hsl(205, 90%, 30%);
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

#tab-content {
    transform: scale(0.92);
    position: relative;
    top: -30px;
}

#B2 {
    position: relative;
    top: -24px;
}
</style>

<script>
import harpiaBar from '@/components/harpiaBar.vue'
import axios from "axios";

export default {
    name: 'Cameras',
    components: {
        harpiaBar
    },
    data() {
        return {
            counter: '',
            group: '1',
            cameraA1: '',
            cameraA4: '',
        }
    },
    created() {
        this.updateCamera()
        this.timer()
        document.title = 'Cameras | Harpia'
    },
    watch: {
      cameraA1(newImg) {

      }
    },
    methods: {
        getImageUrl() {
          //return require('/home/devanir/img/valaris2.jpg')
            return
        },

        async updateCamera() {
          let ip = document.location.href.split("cameras")[0].slice(0, -5) + '8000/'
          let image = ip + 'media/cat.jpg'
          console.log(image)
          await axios
          .get('api/v1/cameras/get_url/')
          .then(response => {
            console.log(response.data.camera1)
            this.cameraA1 = response.data.camera1 + "?" + new Date().getTime()
            this.cameraA4 = response.data.camera4 + "?" + new Date().getTime()
          })
        },


        /* Salva as li em 'tabs', desativa todas,
        ativa a tab selecionada e ajusta o height do div para não conflitar */

        tabSwitcher(tabIndex) {
            this.group = tabIndex
            var tabs = document.querySelectorAll('.tabs li')
            tabs.forEach((tab) => {
                tab.classList.remove('is-active')
            })
            tabs[tabIndex - 1].classList.add('is-active')
            document.getElementById('tab-content').style.height = 'auto'
            console.log(process.env['HOME'])
        },

        /* Se a checkbox estiver ativa a coluna se torna 'is-gapless',
         isso faz com que as imagens fiquem ao lado da outra, ajusta o height do div e o offset do top da imagem B2,
         caso a checkbox seja desmarcada 'is-gapless' é removido, o height e o offset top são ajustados */

        changeOrientation() {
            var checkbox = document.getElementById('orientation')
            var groupB = document.getElementById('camGroupB')
            if (checkbox.checked === true) {
                groupB.classList.add('is-gapless')
                document.getElementById('tab-content').style.height = '95vh'
                document.getElementById('B2').style.top = '0px'
            } else {
                groupB.classList.remove('is-gapless')
                document.getElementById('tab-content').style.height = 'auto'
                document.getElementById('B2').style.top = '-24px'
            }
        },

        /* Quando a página inicia o método timer ativa,
        repetirá o método refreshCameras a cada X milissegundos (usei 10s) */

        timer() {
            clearInterval(this.counter)
            this.counter = setInterval(this.updateCamera, 200)
        },

        /* Salva o url das imagens em variáveis para poder mostrar a mais atualizada,
        adicionando '?v=1' faz com que seja selecionado a versão mais recente do arquivo */
    },
    beforeUnmount() {
        console.log('destroy')
        clearInterval(this.counter)
    },
}

</script>
