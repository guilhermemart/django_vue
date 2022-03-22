<template>
  <div class="vertical-horizontal-center">
    <nav class="navbar is-primary" role="navigation">
      <div class="navbar-brand">
        <router-link to="" @click="goAltave()" class="navbar-item"><img src="@/assets/harpia_logo.png"></router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu }">
        <div class="navbar-start">
            <router-link to="/latest-alerts/1" @click="refresh()"  class="navbar-item">Alerts</router-link>
            <router-link to="/cameras" class="navbar-item">Cameras</router-link>
            <router-link to="/red_zones" class="navbar-item">Red Zones</router-link>
            <router-link to="/overview" class="navbar-item">Overview</router-link>
          <div v-if="show_in_bar == true" class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              Filters
            </a>
            <div class="navbar-dropdown">
              <a class="navbar-item" @click="filterValid()" v-if="filter.valid">
                Valid Alerts<a class="ml-2"><i class="fa-regular fa-eye"></i></a>
              </a>
              <a class="navbar-item" @click="filterValid()" v-else>
                Valid Alerts<a class="ml-2"><i class="fa-regular fa-eye-slash"></i></a>
              </a>
              <a class="navbar-item" @click="filterInvalid()" v-if="filter.invalid">
                Invalid Alerts<a class="ml-2"><i class="fa-regular fa-eye"></i></a>
              </a>
              <a class="navbar-item" @click="filterInvalid()" v-else>
                Invalid Alerts<a class="ml-2"><i class="fa-regular fa-eye-slash"></i></a>
              </a>
              <a class="navbar-item" @click="filterNonClassified()" v-if="filter.non_classified">
                Unclassified<a class="ml-2"><i class="fa-regular fa-eye"></i></a>
              </a>
              <a class="navbar-item" @click="filterNonClassified()" v-else>
                Unclassified<a class="ml-2"><i class="fa-regular fa-eye-slash"></i></a>
              </a>
              <hr class="navbar-divider">
              <a class="navbar-item" @click="filterClear()">
                Clear
              </a>
            </div>
          </div>
        </div>
        <div class="navbar-end">
          <div class="navbar-item">
          <div class="mx-3" v-if="true">
                <span class="mx-2 is-size-4">
                <i class="fas fa-user-circle" /></span>
                <span>{{usuario}}</span>
              </div>
            <div class="buttons">
              <template v-if="$store.state.audio.is_on">
                <div class="button is-primary is-inverted is-outlined" title="Sound off" @click="audioSwitch()">
                <i class="fas fa-volume-high" />
                </div>
              </template>
              <template v-else>
                <div class="button is-dark is-inverted is-outlined" title="Sound on" @click="audioSwitch()">
                <i class="fas fa-volume-xmark" />
                </div>
              </template>
              <template v-if="$store.state.isAuthenticated">
                <button @click="logout()" class="button is-danger is-outlined " title="Logout">
                <i class="fas fa-right-from-bracket" />
                </button>
              </template>
              <template v-else>
                <router-link to="/log-in" class="button is-success is-outlined" title="Login"><i class="fas fa-right-to-bracket" /></router-link>
              </template>

            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>


  </div>

</template>

<script>
import axios from 'axios';

export default {
name:"harpiaBar",
props: {
show_in_bar: {
    type: Boolean,
    default: false
    },
},
data() {
    return {
      showMobileMenu: false,
      filter: {
        valid: true,  // true --> apresenta, false --> esconde
        invalid: true,
        non_classified: true,
        date_start: 0,
        date_end: new Date().getTime(),
        usuario: ""
        }
    }
  },
  methods:{
    refresh(){
       this.filter.date_start = 0
        this.filter.date_end = 2500916953418
        this.$store.commit("save_filter", this.filter)
       this.$router.push("/latest-alerts/1").then(()=> {
            this.$router.go()
        })
    },
    logout() {
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")
            localStorage.removeItem("harpiaUser")
            localStorage.removeItem("userid")
            this.$store.commit('removeToken')
            this.$router.push('/log-in')
        },

    /*
      filterValid, filterInvald e filterNonClassified alteram suas respectivas variáveis locais,
      atualiza a respectiva variável global e deixa o item do dropdown ativo ou desativado, para melhor visualização
      filterClear deixa 3 variáveis locais como true, atualiza a global e ativa os itens do dropdown
     ToDo: campos do filtro nao estão iniciando ativos/inativos
     */
    save_filter(){
        this.$store.commit('save_filter', this.filter)
      },
    filterValid() {
      this.filter.valid = !this.filter.valid
      this.save_filter()
    },
    filterInvalid() {
      this.filter.invalid = !this.filter.invalid
      this.save_filter()
    },
    filterNonClassified() {
      this.filter.non_classified = !this.filter.non_classified
      this.save_filter()
    },
    filterClear() {
      this.filter.valid = true
      this.filter.invalid = true
      this.filter.non_classified = true
      this.save_filter()
    },
    audioSwitch() {
      this.$store.state.audio.is_on = !this.$store.state.audio.is_on
      console.log(this.$store.state.audio.is_on)
    },
    goAltave() {
      window.open("https://www.altave.com.br/")
    },
  },

  mounted() {
    this.filter = this.$store.state.filter
    this.usuario = localStorage.getItem("harpiaUser")
  },
  computed: {

  }
}
</script>