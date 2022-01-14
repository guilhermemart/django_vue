<template>
<p> teste </p>
<div class="column is-6" v-for="alert in GetCurrentPageAlerts" v-bind:key="alert['_id']['$oid']" >



                                </div>
    <div>
        <iframe src="../assets/beep-12.wav" allow="autoplay" id="audio" style="display: none"></iframe>
        <section class="hero has-background-grey-lighter is-fullheight-with-navbar">
            <div class="hero-body">
                <div class="container">
                    <div class="columns is-vcentered is-flex has-horizontal-centered-elements">
                        <div class="column is-5 has-background-white has-rounded-borders">
                            <div class="columns is-vcentered">
                                <div class="column is-1">
                                    <b-icon icon="calendar-month" size="is-medium">
                                    </b-icon>
                                </div>
                                        
                                <div class="column">
                                    <b-datepicker v-model="SelectedDate" :locale="'pt-BR'" placeholder="Selecione uma data..." trap-focus> </b-datepicker>
                                </div>
                                <div class="column is-narrow">
                                    <b-button @click="GetAlertsByDate()" icon-left="magnify" type="is-primary" :disabled="!SelectedDate"><span class="has-text-weight-bold">PESQUISAR</span></b-button>
                                </div>
                                <div class="column is-narrow" v-if="IsDateFiltered">
                                    <b-button @click="GetMostRecentAlerts({pageReset: true})" icon-left="close" type="is-primary"><span class="has-text-weight-bold">REMOVER FILTROS</span></b-button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <br>
                    <p class="has-text-centered has-text-weight-semibold has-text-primary is-size-6">Página {{ CurrentPage }}</p>
                    <br>
                    <div class="columns is-vcentered">
                        <div class="column">
                            <b-button size="is-large" @click="CurrentPage -= 1" icon-right="chevron-left" type="is-primary" :disabled="CurrentPage <= 1" outlined />
                        </div>
                          
                        <div class="column is-11">
                            <div class="columns has-text-black is-multiline" v-if="GetCurrentPageAlerts.length > 0">
                                <div class="column is-6" v-for="alert in GetCurrentPageAlerts" v-bind:key="alert['_id']['$oid']" >

                                    <alert_card :Alert="alert" />

                                </div>
                            </div>
                            <div class="column is-12 has-text-centered is-half-screen-height is-flex has-vertical-centered-text" v-else>
                                <b-icon icon="alert" size="is-large" type="is-dark">
                                </b-icon>
                                <p class="title">
                                    Não há alertas disponíveis.
                                </p>
                            </div>
                        </div>
                        <div class="column">
                            <b-button size="is-large" @click="CurrentPage += 1" icon-right="chevron-right" type="is-primary" :disabled="IsNextPageDisabled" outlined />
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>
<style lang="scss">
.field.has-addons .control:not(:first-child):not(:last-child) .button,
.field.has-addons .control:not(:first-child):not(:last-child) .input,
.field.has-addons .control:not(:first-child):not(:last-child) .select select {
    border-radius: 8px;
}

.has-rounded-borders {
    border-radius: 8px;
    box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1), 0 0px 0 1px rgba(10, 10, 10, 0.02);
}

.has-right-space {
    margin-right: .8vw;
}

.is-half-screen-height {
    height: 50vh;
}

.has-horizontal-centered-elements {
    justify-content: center;
    align-items: center;
}

.has-vertical-centered-text {
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
</style>
<script>
import axios from 'axios'
import alert_card from '@/components/alert_card.vue'
export default {
    components: {
        alert_card,
    },
    data() {
        return {
            Alerts: [],
            SelectedDate: null,
            IsDateFiltered: false,
            LastAlert: null,
            CurrentPage: 1,
            HighestPage: 1,
            AlertsPerPage: 6,
            IsNextPageDisabled: false,
            LockDatabaseSearches: false,
            AlertsWatchdog: null,
            teste: 0,
            reload_or_not: true,  // permite o funcionamento do watching_dog
        }
    },
    computed: {
        GetCurrentPageAlerts() {
            let pageNumber = this.CurrentPage - 1
            let slicedArray = []
            slicedArray = this.Alerts.slice((pageNumber * this.AlertsPerPage), ((pageNumber + 1) * this.AlertsPerPage))
            return slicedArray
        },
        GetLicenseKey() {
            return {"user":localStorage.harpiaUser,"password":localStorage.harpiaPassword}
        },
        GetFilter() {  //filtro que define quais alertas devem aparecer
            return localStorage.filter
        }
      
    },
    watch: {
        CurrentPage: {
            handler() {
                if (!this.LockDatabaseSearches && !this.IsDateFiltered) this.GetAlertsUnsortedPaginated()
                else if (!this.LockDatabaseSearches && this.IsDateFiltered) this.GetAlertsSortedPaginated()
            }
        },
        GetCurrentPageAlerts: {
            handler(alerts) {
                if (alerts.length < 6) this.IsNextPageDisabled = true
                else this.IsNextPageDisabled = false
                
            }        
        },
        WatchingLikeADog:{
           handler(){
               this.WatchingLikeADog
           }       
        }
    },
    methods: {
        get_ip(){
        return process.env.VUE_APP_IP
        //return '192.168.0.24'
        },
        user() {
            return localStorage.harpiaUser
        },
        key() {
            return localStorage.harpiaPassword
        },
        company(){
            return localStorage.harpiaCompany
        },
        WatchingLikeADog(){
            console.log("watch dog atuando")
            axios.get('http://' + this.get_ip() + ':8086/update/'+ this.user()+ "/"+ this.key()).then( elemento => {
                console.log(elemento.data)
                if(this.reload_or_not && this.CurrentPage == 1){
                    this.GetMostRecentAlerts({ pageReset: true })
                }
                else if (localStorage.harpiaCompany == "ocyan"){
                    this.GetMostRecentAlerts({ pageReset: false })
                    this.Play_audio(1)
                }
                else{
                    this.GetMostRecentAlerts({ pageReset: false })
                }
                console.log(elemento)
                this.StartAlertsWatchdog()
                this.WatchingLikeADog()
                }
            ).catch(elemento => {
                console.log(elemento)
                axios.get('http://' + this.get_ip() + ':8086/update/'+ this.user()+ "/"+ this.key()).then( elemento => {
                console.log(elemento.data)
                if(this.reload_or_not && this.CurrentPage == 1){
                    this.GetMostRecentAlerts({ pageReset: true })
                }
                else if (localStorage.harpiaCompany == "ocyan"){
                    this.GetMostRecentAlerts({ pageReset: false })
                    this.Play_audio(1)
                }
                else{
                    this.GetMostRecentAlerts({ pageReset: false })
                }
                console.log(elemento)
                this.StartAlertsWatchdog()
                this.WatchingLikeADog()
                }
            ).catch( elemento => {
                console.log(elemento)
                console.log("watch dog interrompido")
            })  
                })
        },
        Play_audio(vol){
            var audio = new Audio(require("../assets/beep-12.wav"));
            audio.volume = vol
            audio.play()
            return audio
        },
        GetAlertsByDate() {
            this.Alerts = []
            this.StopAlertsWatchdog()
            this.reload_or_not = false
                axios.get('http://'+this.get_ip()+':8085/alerts/date/' + this.SelectedDate.getTime().toString() + '/' + this.GetLicenseKey["password"]+ "/" +this.GetFilter )
                .then(result => {
                    console.log(result)
                    if ("timestamp" in result.data[result.data.length - 1]){
                        this.LastAlert = result.data[result.data.length - 1]['timestamp']}
                    else{
                        this.LastAlert = 0
                    }
                    this.Alerts = result.data
                    this.CurrentPage = 1
                    this.LockDatabaseSearches = false
                    this.IsDateFiltered = true
                })
        },
        GetMostRecentAlerts(options) {
            this.StartAlertsWatchdog()
            this.reload_or_not = true  // volta a mostrar os alertas instantaneos
            // ip+"alerts"+key_recebida_no_login+(true or false para mostrar alertas n classificados) 
            axios.get('http://'+ this.get_ip()+':8085/alerts/' + this.GetLicenseKey["password"] + "/" +this.GetFilter)
                .then(result => {                              
                    if (options.pageReset || this.CurrentPage == 1) {
                        this.Alerts = result.data  // preenchimento da variavel Alerts vai ser usada no alertcard
                        this.CurrentPage = 1
                        }
                    else{
                        var temp = 0
                        if (this.Alerts.length > 0){
                            temp=this.Alerts[0]["timestamp"]
                            var temp2=result.data.reverse()
                            temp2.forEach(alert => {
                                if (alert["timestamp"] > temp){
                                    this.Alerts.unshift(alert)
                                }
                            }
                            )
                        }
                        else {
                            this.Alerts = result.data
                        }
                    }
                    this.LastAlert = this.Alerts[this.Alerts.length -1]['timestamp']
                    this.LockDatabaseSearches = false
                    this.IsDateFiltered = false
                })
        },
        //TODO mudanca de pagina quebra aqui tirar essa gambiarra
        //chamar o axios 2x, que coisa feia, gambiarra da braba
        GetAlertsUnsortedPaginated() {
            axios.get('http://'+ this.get_ip()+':8085/alerts/unfiltered/' + this.LastAlert + '/' + this.key() + "/" + this.GetFilter)
                // axios.get('http://172.19.170.68:8081/alerts/unfiltered/' + this.LastAlert + '/' + this.GetLicenseKey)
                .then(result => {
                    console.log(result)
                    if (result.data.length < 7) this.LockDatabaseSearches = false
                    if ("timestamp" in result.data[result.data.length - 1]){
                        this.LastAlert = result.data[result.data.length - 1]['timestamp']}
                    else{
                        this.LastAlert = 0
                    }
                    result.data.forEach(alert => {
                        this.Alerts.push(alert) })
                }).catch(error=>{
                    console.log(error)
                    axios.get('http://'+ this.get_ip()+':8085/alerts/unfiltered/' + this.LastAlert + '/' + this.key() + "/" + this.GetFilter)
                .then(result => {
                    console.log(result)
                    if (result.data.length < 7) this.LockDatabaseSearches = true
                    if ("timestamp" in result.data[result.data.length - 1]){
                        this.LastAlert = result.data[result.data.length - 1]['timestamp']}
                    else{
                        this.LastAlert = 0
                    }
                    result.data.forEach(alert => {
                        this.Alerts.push(alert) })
                })
                })
        },
        GetAlertsSortedPaginated() {
            axios.get('http://'+ this.get_ip()+':8085/alerts/filtered/' + this.LastAlert + '/' + this.SelectedDate.getTime() + '/' + this.key() + "/" + this.GetFilter)
                // axios.get('http://172.19.170.68:8081/alerts/filtered/' + this.LastAlert + '/' + this.SelectedDate.getTime() + '/' + this.GetLicenseKey)
                .then(result => {
                    console.log(result)
                    if (result.data.length < 7) this.LockDatabaseSearches = true
                    this.LastAlert = result.data[result.data.length - 1]['timestamp']
                    result.data.forEach(alert => { this.Alerts.push(alert) })
                })
        },
        StartAlertsWatchdog() {
            clearInterval(this.AlertsWatchdog)
            this.AlertsWatchdog = setInterval(() => { 
                this.GetMostRecentAlerts({ pageReset: false }) 
                }, 60000)
        },
        StopAlertsWatchdog() {
            clearInterval(this.AlertsWatchdog)
        },
        forceRerender_card(){
            this.alert_card_key += 1;
        }
    },
    beforeCreate(){
        if (!localStorage.getItem('harpiaPassword')||!localStorage.getItem('harpiaUser')){
            window.location.href = "http://"+this.get_ip()+":8080/login";
        }
    },
    created() {
        this.GetMostRecentAlerts({ pageReset: false })
        this.CurrentPage = 1
        this.WatchingLikeADog(true)
        localStorage.habilita_audio = true
    },
    beforeDestroy(){
        if(localStorage.harpiaCompany == "samarco"){
            localStorage.harpiaUser = false;
            localStorage.harpiaPassword = false;
        }
    }
}
</script>