<template>
  <div class="container" v-if="inited" >
     <div class="row row--underlined" >
      <div class="block">
        <h1>ABOUT <br/>THE PROJECT</h1>

         

      </div>
    </div>
  </div>
</template>

<script>


export default {
  name: 'about_project',
  components: {

  },
  watch: {
    text(  ) {
      this.inited = true;
    },
  },
  data(){
    return{
      text:null,
      inited:true,
    }
  },
  mounted(){

  },  
  methods:{
   
  }
}
</script>

<style lang="scss">
@import '~@/assets/scss/main';



</style>
