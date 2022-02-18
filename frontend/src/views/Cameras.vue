<template>
    <div id="main-div" class="overlay">
        <harpiaBar/>

        <!-- Div com as tabs.
         Função tabSwitcher troca o conteúdo -->

        <div class="tabs is-centered is-toggle mt-1 is-small">
          <ul>
            <li class="is-active mr-4" @click="tabSwitcher('1')">
              <a id="tabs">
                <span>Área A</span>
              </a>
            </li>
            <li class="mr-4" @click="tabSwitcher('2')">
              <a id="tabs">
                <span>Área B</span>
              </a>
            </li>
            <li @click="tabSwitcher('3')">
              <a id="tabs">
                <span>Área C</span>
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
                    <img id="camA1" src="@/assets/valaris1.jpg" width="980" alt="camera 1"/>
                    <!-- A primeira imagem está sendo pega de uma pasta 'images' que fica na HOME
                    A página não funciona sem esta pasta e a imagem. Descomente para testar!
                    <img id="camA1" src="../../../../../images/valaris1.jpg" width="980" alt="camera 1"/>
                    -->
                </div>
                <div class="column is-half">
                    <img id="camA2" src="@/assets/valaris2.jpg" width="980" alt="camera 2"/>
                </div>
                <div class="column is-half ">
                    <img id="camA3" src="@/assets/valaris3.jpg" width="980" alt="camera 3"/>
                </div>
                <div class="column is-half">
                    <img id="camA4" src="@/assets/valaris4.jpg" width="980" alt="camera 4"/>
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
    top: -40px;
}

#B2 {
    position: relative;
    top: -24px;
}
</style>

<script>
import harpiaBar from '@/components/harpiaBar.vue'

export default {
    name: 'Cameras',
    components: {
        harpiaBar
    },
    data() {
        return {
            counter: '',
            group: '1',
        }
    },
    created() {
        this.timer()
    },
    methods: {

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
            this.counter = setInterval(this.refreshCameras, 10000)
        },

        /* Salva o url das imagens em variáveis para poder mostrar a mais atualizada,
        adicionando '?v=1' faz com que seja selecionado a versão mais recente do arquivo */

        refreshCameras() {
            if (this.group === '1') {
                let camA1 = document.getElementById('camA1').src
                camA1 = camA1 += '?v=1'
                console.log(camA1)
                let camA2 = document.getElementById('camA2').src
                camA2 = camA2 += '?v=1'
                console.log(camA2)
                let camA3 = document.getElementById('camA3').src
                camA3 = camA3 += '?v=1'
                console.log(camA3)
                let camA4 = document.getElementById('camA4').src
                camA4 = camA4 += '?v=1'
                console.log(camA4)
            } else if (this.group === '2') {
                let camB1 = document.getElementById('camB1').src
                camB1 = camB1 += '?v=1'
                console.log(camB1)
                let camB2 = document.getElementById('camB2').src
                camB2 = camB2 += '?v=1'
                console.log(camB2)
            } else if (this.group === '3') {
                console.log('GROUP C')
                let camC1 = document.getElementById('camC1').src
                camC1 = camC1 += '?v=1'
                let camC2 = document.getElementById('camC2').src
                camC2 = camC2 += '?v=1'
                let camC3 = document.getElementById('camC3').src
                camC3 = camC3 += '?v=1'
                let camC4 = document.getElementById('camC4').src
                camC4 = camC4 += '?v=1'
            }
        },
    },
    beforeUnmount() {
        console.log('destroy')
        clearInterval(this.counter)
    },
}

</script>
