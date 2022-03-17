<!--Pagina de resumo de cada camera, nessa view é possível verificar a imagem base de cada camera-->
<!-- um resumo das red zones conectadas aquela camera-->
<template>
    <div class="camera_page">
    {{camera}}
        <div class="columns is-multiline">


            <div class="column is-3">
                <h2 class="subtitle">Detalhes da camera</h2>

                <p><strong>Name: </strong>{{ camera.name }}</p>

                <div class="field has-addons mt-6">
                    <div class="control">
                    <p class='fake_button'> {{is_active()}} </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.fake_button{
        background: -webkit-linear-gradient(top, #CCB5B6 20%, #274936 70%);
        font-family: sans-serif;
        font-size: 25px;
        text-align: center;
        line-height: 40px;
        color: #96F256;
        border-radius: 10px;
        box-shadow: 0 2px 5px 3px black;
    }

</style>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: 'Camera',
    data() {
        return {
            camera: {
            },
        }
    },
    mounted() {
        console.log("iniciando camera")
        this.getCamera()
        document.title = 'Camera | Harpia'
    },
    methods: {
        is_active() {
        return this.camera.ativa
        },
        async getCamera() {
            this.$store.commit('setIsLoading', true)
            const slug_cam = this.$route.params.slug_cam
            await axios
                .get(`/api/v1/red_zone/${slug_cam}`)
                .then(response => {
                    this.camera = response.data
                    document.title = this.camera.name + ' | Harpia'
                })
                .catch(error => {
                    console.log("erro de axios")
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },

    }
}
</script>