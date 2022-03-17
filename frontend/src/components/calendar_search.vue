<template>
  <div>
    <div class="control">
  <label class="radio">
    <input v-model="isRange" value="false" type="radio" name="day">
    dia
  </label>
  <label class="radio">
    <input v-model="isRange" value="false" type="radio" name="period">
    periodo
  </label>
</div>
    <Datepicker v-model="date" :range="isRange" :partialRange='false'/>
    {{date}}
    <hr>
    {{isRange}}
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
        last_date: new Date(),
        isRange:''
    }
  },
    computed:{
    dateSelect(){
      return this.date
    }

  },
  watch:{    
  dateSelect:{
    handler(){      
      this.toTimestamp()
    }  
  }  
  },
  methods:{
    toTimestamp(){
      let justDate0=new Date(this.date[0]).toDateString()
      this.date[0]=new Date(justDate0).getTime()
      let justDate1=new Date(this.date[1]).toDateString()
      this.date[1]=new Date(justDate1).getTime()-99
      alert(this.date)

    }
  }
};
</script>