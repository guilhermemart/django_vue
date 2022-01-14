<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <alert_card/>
    <!--<HelloWorld msg="Welcome to Your Vue.js App"/>-->
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import alert_card from '@/components/alert_card.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld,
    alert_card
  }
}
</script>
