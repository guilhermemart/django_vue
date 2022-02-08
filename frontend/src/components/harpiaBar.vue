<template>
  <div class="vertical-horizontal-center">
    <nav class="navbar is-primary" role="navigation">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><img src="@/assets/harpia_logo.png"></router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
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
data() {
    return {
      showMobileMenu: false,

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
  },

  mounted() {
  },
  computed: {

  } 
}
</script>