<template>
  <div>
    <Datepicker v-model="date" range :partialRange='false'/>
    {{date}}
    <hr>
  </div>
</template>

<script>
import { ref } from "vue";
import Datepicker from "vue3-date-time-picker";
import "vue3-date-time-picker/dist/main.css";

export default {
  name: "calendar_search",
  components: {
    Datepicker,
  },
  data(){
    return{
        date: new Date(),
        last_date: new Date()
    }
  },
  watch:{
  date(){
  alert("teste")
  }
  /*status(date){
    if(date!=last_date){
    this.last_date=this.date
   console.log(this.date[0])}
  }*/
  },
};
</script>