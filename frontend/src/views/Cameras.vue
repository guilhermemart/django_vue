<template>
    <div style="height: 100%" v-bind:style="{backgroundColor: color}">
        <harpiaBar/>
        <div class="tabs is-centered is-toggle mt-2">
          <ul>
            <li class="is-active" @click="tabSwitcher('1')">
              <a id="tabs" class="mr-2">
                <span>Área A</span>
              </a>
            </li>
            <li @click="tabSwitcher('2')">
              <a id="tabs" class="mr-2">
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

        <div id="tab-content" class=" ml-3 mr-3">
            <div id="camsA" v-if="group=='1'" class="columns is-multiline is-gapless">
                <div class="column is-half">
                    <img src="@/assets/cam1.jpg" alt="camera 1"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/cam2.jpg" alt="camera 2"/>
                </div>
                <div class="column is-half ">
                    <img src="@/assets/cam3.jpg" alt="camera 3"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/cam4.jpg" alt="camera 4"/>
                </div>
            </div>

            <div id="camsB" v-if="group=='2'" class="columns is-multiline is-gapless">
                <div class="column is-full">
                    <img src="@/assets/cam5.jpg" alt="camera 5"/>
                </div>
                <div class="column is-full">
                    <img src="@/assets/cam6.jpg" alt="camera 6"/>
                </div>
            </div>

            <div id="camsC" v-if="group=='3'" class="columns is-multiline is-gapless">
                <div class="column is-half">
                    <img src="@/assets/patio01.jpg" alt="camera 7"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/patio02.jpg" alt="camera 8"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/cam5.jpg" alt="camera 9"/>
                </div>
                <div class="column is-half">
                    <img src="@/assets/cam6.jpg" alt="camera 10"/>
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
            color: 'hsl(200, 2%, 2%)',
            group: '1',
        }
    },
    methods: {
        tabSwitcher(g) {
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

<style>
#tabs {
    width: 12vw;
    background: hsl(205, 90%, 50%);
    border-radius: 24px;
}

.is-active {
    transform: scale(0.83);
}

</style>