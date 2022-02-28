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
      <input class="input is-focused" v-model="temp" type="text" placeholder="Insert Redzone names">

    </section>
    <footer class="modal-card-foot">
      <button class="button is-success" @click="save">Save Redzone</button>
      <button class="button is-danger isRight" @click="showModal()">Cancel</button>
    </footer>
  </div>
</div>

<div class="columns">
<div class="  column is-2">
 <button class="button">
    <span class="icon">
      <i class="fab fa-github"></i>
    </span>
    <span>GitHub</span>
  </button>
<p><button class="button is-danger is-outlined is-fullwidth focus mt-1" @click="showModal()" >
<span class="icon">
      <i class="fas fa-eraser"></i>
    </span><span>Clean</span>
</button></p>
<p><button class="button is-warning is-outlined is-fullwidth focus mt-1" @click="showModal()" ><span class="icon">
      <i class="fas fa-undo"></i>
    </span><span>UNDO</span></button></p>
<p><button class="button is-success is-outlined is-fullwidth focus mt-1" @click="showModal()" ><span class="icon">
      <i class="fas fa-save"></i>
    </span><span>SAVE</span></button></p>
<p><button class="button is-dark is-outlined is-fullwidth focus mt-1" @click="showModal()" ><span class="icon">
      <i class="fas fa-upload"></i>
    </span><span>LOAD</span></button></p>

<p><button class="button is-success is-outlined is-fullwidth focus mt-1" @click="showModal()" >ACTIVE</button></p>
</div>
<div class="column is-4">
<p>Redzone Name: {{rdName}}</p>
</div>
</div>
 <div>
  <span class="icon has-text-danger">  
    <i class="far fa-user"></i>
  </span>
  <br>
  <span class="icon">  
    <i class="far fa-2x fa-flag"></i>
  </span>
    <br>
  <span class="icon">  
    <i class="fas fa-spinner fa-pulse"></i>
  </span>
  <br>
   <span class="icon">  
    <i class="fas fa-spinner"></i>
  </span>
 </div>

<div class="select is-dark">
  <select>
    <option>LOAD</option>
    <option>With options</option>
  </select>
</div>
</div>
    
</template>
<style lang="scss">
.modal-card{
    border-style: solid;
    border-radius: 2.5vh;
    border-color: black;
    border-width: 0.1vh;    
    
}
.modal-card-head{
    background-color: #180474 !important;    
}
.modal-card-title{
    color: white !important;
}
.isRight{
    float: right;
    margin-left: 63%;
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
            show:false,
            rdName:'',
            temp:''
        }
    },
    computed: {
         
    },
    watch:{
      

    },
    methods: {
        save(){
            this.rdName=this.temp
            this.showModal()

        },
        showModal(){            
            this.show=!this.show
            
        }
    },
}
</script>
