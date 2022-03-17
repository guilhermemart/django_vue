<template>
  <div class="vertical-horizontal-center">
    <nav class="navbar is-primary" role="navigation">
      <div class="navbar-brand">
        <div class="mt-1" @click="logout()">
          <router-link to="/" class="navbar-item"><img src="@/assets/harpia_logo.png"></router-link>
        </div>
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
              <a class="navbar-item" @click="filterValid()" v-if="filter.valid">
                Alertas validos <a class="ml-2"><i class="fa-regular fa-eye"></i></a>
              </a>
              <a class="navbar-item" @click="filterValid()" v-else>
                Alertas validos <a class="ml-2"><i class="fa-regular fa-eye-slash"></i></a>
              </a>
              <a class="navbar-item" @click="filterInvalid()" v-if="filter.invalid">
                Alertas invalidos <a class="ml-2"><i class="fa-regular fa-eye"></i></a>
              </a>
              <a class="navbar-item" @click="filterInvalid()" v-else>
                Alertas invalidos <a class="ml-2"><i class="fa-regular fa-eye-slash"></i></a>
              </a>
              <a class="navbar-item" @click="filterNonClassified()" v-if="filter.non_classified">
                Não classificados <a class="ml-2"><i class="fa-regular fa-eye"></i></a>
              </a>
              <a class="navbar-item" @click="filterNonClassified()" v-else>
                Não classificados <a class="ml-2"><i class="fa-regular fa-eye-slash"></i></a>
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
              <template v-if="true">
                <router-link to="/audio" class="button is-primary is-inverted is-outlined" title="Sound off">
                <i class="fas fa-volume-high" />                    
                </router-link>
              </template>
              <template v-else>
                <router-link to="/config-som" class="button is-dark is-inverted is-outlined" title="Sound on">
                <i class="fas fa-volume-xmark" />                    
                </router-link>
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
        date_end: new Date().getTime()
        }
    }
  },
  methods:{
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
    }
  },

  mounted() {
    this.filter = this.$store.state.filter
  },
  computed: {

  } 
}
</script>