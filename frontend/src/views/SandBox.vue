<template>
<div>
<harpiaBar/>
<div class="modal"  :class="{'is-active': show}" >
  
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">Redzone name</p>
      <button class="delete" @click="showModal()" aria-label="close"></button>
    </header>
    <section class="modal-card-body">
      <!-- Content ... -->
    </section>
    <footer class="modal-card-foot">
      <button class="button is-success">Save Redzone</button>
      <button class="button" @click="showModal()">Cancel</button>
    </footer>
  </div>
</div>
<button @click="showModal()" >
  show{{show}}
</button>


</div>
    
</template>
<style lang="scss">
.modal{
    
    
}
.modal-card-head{
    background-color: #180474 !important;    
}
.modal-card-title{
    color: white !important;
}

</style>


<script>
import harpiaBar from '@/components/harpiaBar.vue'
export default {
    name:'SandBox',
    components:{
        harpiaBar
    },
    data(){
        return{
            show:false
        }
    },
    methods: {
        showModal(){
            alert()
            this.show=!this.show
        }
    },
}
</script>
