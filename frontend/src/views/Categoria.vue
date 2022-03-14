<!--Pagina de resumo de cada categoria, nessa view é possível verificar a categoria-->
<!-- um resumo dos alertas daqela categoria-->
<template>
    <div class="categoria_page">
    {{categoria}}
        <div class="columns is-multiline">


            <div class="column is-3">
                <h2 class="subtitle">Detalhes da camera</h2>

                <p><strong>Name: </strong>{{ categoria.name }}</p>


            </div>
        </div>
    </div>
</template>

<style>

</style>

<script>
import axios from 'axios'

export default {
    name: 'Categoria',
    data() {
        return {
            categoria: {
            },
        }
    },
    mounted() {
        console.log("iniciando categoria")
        this.getCategoria()
        document.title = 'Camera | Harpia'
    },
    methods: {
        async getCategoria() {
            this.$store.commit('setIsLoading', true)
            const slug_categoria = this.$route.params.slug_categoria
            await axios
                .get(`/api/v1/1111/${slug_categoria}`)
                .then(response => {
                    this.categoria = response.data
                    document.title = this.categoria.name + ' | Harpia'
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