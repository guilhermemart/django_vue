<template>
    <!--{{audio}}-->
    <div class="audio_page">
        <div class="control">
            <label class="radio">
            <input v-model="audio.is_on" value="true" type="radio" name="audio_enable" checked>
            Ligado
            </label>
            <label class="radio">
            <input v-model="audio.is_on" value="false" type="radio" name="audio_enable" >
            Desligado
            </label>
        </div>
        <label class="checkbox">
            <input v-model="audio.is_instantaneo" value="true" type="checkbox" checked>
            Instantaneo
        </label>
        <label class="checkbox">
            <input v-if="audio.is_recorrente=='true'" v-model="audio.has_delay" value="true" type="checkbox" checked disabled>
            <input  v-else v-model="audio.has_delay" value="true" type="checkbox" >
            Atraso 5 minutos
        </label>
        <div class="control">
            <label class="radio">
                <input v-model="audio.is_recorrente" value="true" v-on:click="SetRecorrent()" type="radio" name="timer" checked>
                Recorrente
            </label>
            <label class="radio">
                <input v-model="audio.is_recorrent" value="false" type="radio" name="timer">
                Alarme único
            </label>
        </div>
        <p v-if="audio.is_on=='false'"> Alarme sonoro desabilitado </p>
        <p v-else >Alertas sonoros abilitados</p>
        <button @click="save_audio()">SAVE</button>

</div>
</template>
<script>

export default {
    name: 'Alerta',
    data() {
        return {
            audio: {
                is_on: "true",
                is_instantaneo: "true",
                is_recorrente: "true",
                has_delay: "true",
            },
            remove_option: "false"
        }
    },
    mounted() {
        this.audio = this.$store.state.audio
        document.title = 'Audio | Harpia'
    },
    methods: {
        SetRecorrent(){
            this.audio.has_delay = "true"
            this.audio.remove_option = "true"
            return "true"
        },
        save_audio(){
            this.$store.commit('save_audio', this.audio)
            toast({
                message: 'The audio config was saved',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-center',
            })
        },
    }
}
</script>