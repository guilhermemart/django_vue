<template>

    <div class="alert_page">
        <div class="columns is-multiline">
            <div class="column is-9">
                <figure class="image mb-6">
                    <img v-bind:src="Alert.get_image">
                </figure>
                <h2 class="title">Adicionado:</h2>
                <h2 class="subtitle">{{ Alert.date_added }}</h2>
                <textarea>Notas: {{ Alert.description }}</textarea>
            </div>

            <div class="column is-3">
                <h2 class="subtitle">Detalhes do Alerta</h2>

                <p><strong>Id: </strong>{{ Alert.identificador }}</p>

                <div class="field has-addons mt-6">


                    <div class="control">
                    <p class='fake_button'> {{get_thumb()}} </p>
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
    name: 'Alerta',
    data() {
        return {
            Alert: {},
            quantity: 1
        }
    },
    mounted() {

        console.log("iniciando")
        this.getAlert()
        document.title = 'Alerta | Harpia'
    },
    methods: {
        get_thumb() {
            if (this.Alert.thumb_up==false){
                if(this.Alert.thumb_down==false){
                    return "n_classificado"
                }
                else{
                    return "desaprovado"
                }
            }
            else{
                return "aprovado"
            }
        },
        async getAlert() {
            this.$store.commit('setIsLoading', true)
            const category_slug = this.$route.params.category_slug
            const alert_slug = this.$route.params.alert_slug
            await axios
                .get(`/api/v1/alerts/${category_slug}/${alert_slug}`)
                .then(response => {
                    this.Alert = response.data
                    console.log("response")
                    document.title = this.Alert.id + ' | Harpia'
                })
                .catch(error => {
                    console.log("erro de axios")
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
        },
        addToCart() {
            this.quantity += 1
        }
    }
}
</script>