<template>
    <div id="main-div" class="overlay">
        <harpiaBar/>

        <!-- Div com as tabs.
         Função tabSwitcher troca o conteúdo -->

        <div class="tabs is-centered is-toggle mt-2 is-small">
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

        <div id="switch" v-if="group=='2'">
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

        <div id="tab-content" class="">
            <div id="camsA" v-if="group=='1'" class="columns is-multiline is-gapless">
                <div class="column is-half">
                    <img src="@/assets/valaris1.jpg" width="1000" alt="camera 1"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/valaris2.jpg" width="1000" alt="camera 2"/>
                </div>
                <div class="column is-half ">
                    <img src="@/assets/valaris3.jpg" width="1000" alt="camera 3"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/valaris4.jpg" width="1000" alt="camera 4"/>
                </div>
            </div>

            <div id="camsB" v-if="group=='2'" class="columns is-multiline">
                <div class="column is-half is-offset-one-quarter">
                    <img src="@/assets/valaris1.jpg" width="942" alt="camera 5"/>
                </div>
                <div class="column is-half is-offset-one-quarter">
                    <img src="@/assets/valaris3.jpg" width="942" alt="camera 6"/>
                </div>
            </div>

            <div id="camsC" v-if="group=='3'" class="columns is-multiline is-gapless">
                <div class="column is-half">
                    <img src="@/assets/cam1.jpg" width="942" alt="camera 7"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/cam3.jpg" width="942" alt="camera 8"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/valaris1.jpg" width="942" alt="camera 9"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/valaris4.jpg" width="942" alt="camera 10"/>
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
    height: 2em;
    background: hsl(205, 90%, 50%);
    border-radius: 24px;
    transition: .3s;
}

.is-active {
    transform: scale(1.1);
    font-size: 15px;
}

.slider-text {
  color: white;
  position: absolute;
  font-size: 10px;
  right: 7.2em;
  top: 8em;
}

.switch {
  position: absolute;
  width: 42px;
  height: 14px;
  right: 4em;
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
  transition: .2s;
}

input:checked + .slider {
  background-color: hsl(205, 90%, 30%);
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

#tab-content {
    transform: scale(0.96);
    position: relative;
    top: -30px
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
            group: '1',
        }
    },
    methods: {

        /* Salva as li em 'tabs', desativa todas,
        ativa a tab selecionada e ajusta o height do div para não conflitar*/

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
         isso faz com que as imagens fiquem ao lado da outra, e ajusta o height do div,
         caso a checkbox seja desmarcada 'is-gapless' é removido e o height é ajustado*/

        changeOrientation() {
            var checkbox = document.getElementById('orientation')
            var groupB = document.getElementById('camsB')
            if (checkbox.checked == true) {
                groupB.classList.add('is-gapless')
                document.getElementById('tab-content').style.height = '88.1vh'
            } else {
                groupB.classList.remove('is-gapless')
                document.getElementById('tab-content').style.height = 'auto'
            }
        }
    },
}

</script>
