<template>
  <div class="vertical-horizontal-center">
    <nav class="navbar is-primary" role="navigation">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><img src="@/assets/harpia_logo.png"></router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu }">
        <div class="navbar-start">
            <router-link to="/latest-alerts/1" class="navbar-item">Alertas</router-link>
            <router-link to="/cameras" class="navbar-item">Cameras</router-link>
            <router-link to="/red_zones" class="navbar-item">Red Zones</router-link>
            <router-link to="/resumo" class="navbar-item">Resumo</router-link>
          <div v-if="show_in_bar == true" class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              Filtros
            </a>
            <div class="navbar-dropdown">
              <a id="field-valid" class="navbar-item" @click="filterValid()">
                Alertas validos
              </a>
              <a id="field-invalid" class="navbar-item" @click="filterInvalid()">
                Alertas invalidos
              </a>
              <a id="field-nonclass" class="navbar-item" @click="filterNonClassified()">
                Não classificados
              </a>
              <hr class="navbar-divider">
              <a class="navbar-item" @click="filterClear()">
                Limpar filtros
              </a>
            </div>
          </div>
        </div>
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">
                <button @click="logout()" class="button is-danger">Log out</button>
              </template>
              <template v-else>
                <router-link to="/log-in" class="button is-light">Log in</router-link>
              </template>
              <template v-if="true">
                <router-link to="/audio" class="button is-success">
                    <span class="icon"><img alt="sound_logo" src="../assets/sound_logo.png"></span>
                    <span>Audio</span>
                </router-link>
              </template>
              <template v-else>
                <router-link to="/config-som" class="button is-success">
                    <span class="icon"><img alt="sound_off_logo" src="../assets/sound_off_logo.png"></span>
                    <span>Audio</span>
                </router-link>
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
      date_end: new Date().getTime()
        }
    }
  },
  methods:{
    logout() {
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")
            localStorage.removeItem("username")
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
      if (this.filter.valid){
        document.getElementById("field-valid").classList.add("is-active")
      } else {
        document.getElementById("field-valid").classList.remove("is-active")
      }
    },
    filterInvalid() {
      this.filter.invalid = !this.filter.invalid
      this.save_filter()
      if (this.filter.invalid){
        document.getElementById("field-invalid").classList.add("is-active")
      } else {
        document.getElementById("field-invalid").classList.remove("is-active")
      }
    },
    filterNonClassified() {
      this.filter.non_classified = !this.filter.non_classified
      this.save_filter()
      if (this.filter.non_classified){
        document.getElementById("field-nonclass").classList.add("is-active")
      } else {
        document.getElementById("field-nonclass").classList.remove("is-active")
      }
    },
    filterClear() {
      this.filter.valid = true
      this.filter.invalid = true
      this.filter.non_classified = true
      this.save_filter()
      document.getElementById("field-valid").classList.add("is-active")
      document.getElementById("field-invalid").classList.add("is-active")
      document.getElementById("field-nonclass").classList.add("is-active")
    }
  },

  mounted() {
  this.filter = this.$store.state.filter
  },
  computed: {

  } 
}
</script>