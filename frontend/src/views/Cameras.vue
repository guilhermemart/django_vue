<template>
    <div v-bind:style="{backgroundColor: color}">
        <harpiaBar/>
        dev ainda não está na área<br>
        Área de texto acima das cameras

        <div class="tabs is-fullwidth is-toggle">
          <ul>
            <li class="is-active" @click="tabSwitcher('1', $event)">
              <a>
                <span>Área A</span>
              </a>
            </li>
            <li @click="tabSwitcher('2', $event)">
              <a>
                <span>Área B</span>
              </a>
            </li>
            <li @click="tabSwitcher('3', $event)">
              <a>
                <span>Área C</span>
              </a>
            </li>
          </ul>
        </div>

        <div id="tab-content">
            <div id="camsA" v-if="group=='1'">
                <div id="camsA1" class="columns is-multiline">
                    <div class="column is-half">
                        <img src="@/assets/cam1.jpg" alt="camera 1"/>
                    </div>
                    <div class="column is-half">
                        <img src="@/assets/cam2.jpg" alt="camera 2"/>
                    </div>
                </div>

                <div id="camsA2" class="columns is-multiline">
                    <div class="column is-half">
                        <img src="@/assets/cam3.jpg" alt="camera 3"/>
                    </div>
                    <div class="column is-half">
                        <img src="@/assets/cam4.jpg" alt="camera 4"/>
                    </div>
                </div>
            </div>

            <div id="camsB" class="columns is-multiline" v-if="group=='2'">
                <div class="column is-half">
                    <img src="@/assets/cam5.jpg" alt="camera 3"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/cam6.jpg" alt="camera 4"/>
                </div>
            </div>

            <div id="camsC" v-if="group=='3'">
                <div id="camsC1" class="columns is-multiline">
                    <div class="column is-half">
                        <img src="@/assets/logo.png" alt="camera 1"/>
                    </div>
                    <div class="column is-half">
                        <img src="@/assets/cam2.jpg" alt="camera 2"/>
                    </div>
                </div>

                <div id="camsC2" class="columns is-multiline">
                    <div class="column is-half">
                        <img src="@/assets/cam3.jpg" alt="camera 3"/>
                    </div>
                    <div class="column is-half">
                        <img src="@/assets/sound_logo.png" alt="camera 4"/>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import harpiaBar from '@/components/harpiaBar.vue'

export default {
    name: 'Cameras',
    components: {
        harpiaBar
    },
    data() {
        return {
            color: '#16161c',
            group: '1',
        }
    },
    methods: {
        tabSwitcher(g, event) {
            this.group = g
            const tabs = document.querySelectorAll('.tabs li')
            tabs.forEach((tab) => {
                tab.classList.remove('is-active')
            })
            tabs[g - 1].classList.add('is-active')
        }
    },
}

</script>