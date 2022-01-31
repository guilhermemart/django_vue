<template>


  <div>
    <nav class="navbar is-primary" role="navigation">
      <div class="navbar-brand">
        <p class="navbar-item">
          <img src="@/assets/harpia_logo.png">
        </p>
      </div>
      

      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Beholder</strong></router-link>
        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true">a</span>
          <span aria-hidden="true">a</span>
          <span aria-hidden="true">a</span>
        </a>
      </div>
      <div class="navbar-menu" id="navbar-menu" v-bind:class="{'is-active': showMobileMenu }">
        <div class="navbar-start">
            <router-link to="/latest-alerts/1" class="navbar-item">Alertas</router-link>
            <router-link to="/cameras" class="navbar-item">Cameras</router-link>
            <router-link to="/tupan" class="navbar-item">Tupans</router-link>
        </div>
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">
                <button @click="logout()" class="button is-danger">Log out</button>
                <router-link to="/log-in" class="button is-light">log out</router-link>
              </template>
              <template v-else>
                <router-link to="/log-in" class="button is-light">Log in</router-link>
              </template>
              <template v-if="true">
                <router-link to="/config-som" class="button is-success">
                    <span class="icon"><img alt="sound_logo" src="../assets/sound_logo.png"></span>
                    <span>Audio ({{ cartTotalLength }})</span>
                </router-link>
              </template>
              <template v-else>
                <router-link to="/config-som" class="button is-success">
                    <span class="icon"><img alt="sound_off_logo" src="../assets/sound_off_logo.png"></span>
                    <span>Audio ({{ cartTotalLength }})</span>
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

      <router-view/>

  </div> 
  
</template>

<script>
import axios from 'axios';

export default {
name:"harpiaBar",
data() {
    return {
      showMobileMenu: false,
      cart: {
        items: []
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
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
        axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    this.cart = this.$store.state.cart
  },
  computed: {
      cartTotalLength() {
          let totalLength = 0
          for (let i = 0; i < this.cart.items.length; i++) {
              totalLength += this.cart.items[i].quantity
          }
          return totalLength
      }
  } 
}
</script>