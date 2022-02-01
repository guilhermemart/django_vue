<template>
    <div class="page-log-in">
    <div class="has-background-primary">
        <div class="columns vertical-horizontal-center ">
        <div class="column is-3">
            <form @submit.prevent="submitForm" class="has-text-left">  
                <figure class="image is-3by2 is-fullwidth">
                    <img class="has-ratio" :src="require('@/assets/harpia_logo_alt.png')">
                </figure>              
                <div class="field">
                    <p class="control">
                        <span class=" has-text-white-bis is-size-6">Login</span>
                        <input class="input is-hovered has-background-primary has-text-white-bis" type="text" v-model="username"  />
                    </p>   
                </div>
                <div class="field">               
                    <span class=" has-text-white-bis is-size-6">Password</span>
                    <input class="input is-hovered has-background-primary has-text-white-bis" v-model="password" type="password"  />                
                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                    <div class="field">
                    <br/>
                        <div class="control">
                            <button class="button is-dark is-centered">Log in</button>
                        </div>
                    </div>

                    <!--<hr>

                    Or <router-link to="/sign-up">click here</router-link> to sign up!-->
               </div>
            </form>
            </div>
        </div>      
    </div>
    </div>
</template>

<style lang="scss" scoped>

.has-custom-width {
    width: 75%
}

.vertical-horizontal-center {
    height: 100vh;
    padding: 0;
    justify-content: center;
    align-items: center;
}
</style>
<script>
import axios from 'axios'

import { Field, Form, ErrorMessage } from 'vee-validate';
export default {
    name: 'LogIn',
    components: {
  },
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    mounted() {
        document.title = 'Log In | Harpia'
    },
    methods: {
        async submitForm() {
            axios.defaults.headers.common["Authorization"] = ""

            localStorage.removeItem("token")

            const formData = {
                username: this.username,
                password: this.password
            }

            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token

                    this.$store.commit('setToken', token)

                    axios.defaults.headers.common["Authorization"] = "Token " + token

                    localStorage.setItem("token", token)

                    const toPath = this.$route.query.to || '/latest-alerts/1'

                    this.$router.push(toPath)
                })
                .catch(error => {
                    this.errors=[]
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else {
                        this.errors.push('Something went wrong. Please try again')

                        console.log(JSON.stringify(error))
                    }
                })
        }
    }
}
</script>