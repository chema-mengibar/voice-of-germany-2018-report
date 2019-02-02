<template>
  <div class="container" v-if="inited" >
     <div class="row row--underlined" >
      <div class="block">
        <h1>THE PROJECT</h1>
      </div>
    </div>

  <div class="row row_pb-40"  >
    <div class="block">
      <h2>The Project</h2>
      <p>The project consists of two main blocks. On one part of project consist in the ETL processes and data manipulation, and on the other the visualization part of the processed data.</p>
    </div>
  </div>

  <div class="row row__1a1">
    <div class="block">
      <h3>Data Processing</h3>
      <p>
        The result of part of data processing is a series of scripts that work with different data-sources
         and libraries.
      </p>
      <p>Tools:</p>
      <p>
        - Selenium ( WebScraping )  <br/>
        - Python    <br/>
          - numpy, pandas, matplotlib   <br/>
          - langdetect, langid, guess_language
      </p>
    </div>
    <div class="block">
      <h3>Data Visualization</h3>
      <p>
       The result of the visualization part is a responsive-website in which the data is loaded and displayed dynamically.
      </p>
      <p>Tools:</p>
      <p>
        - Vue.js  <br/>
        - D3.js  <br/>
        - PHP
      </p>
    </div>

  </div>


  <!-- <div class="row row__1a1">
    <div class="block">
      <h3>ETL Tasks</h3>
      <p>
        The result of part of data processing is a series of scripts that work with different data-sources
         and libraries.
      </p>
      <p>Tools:</p>
      <p>
        - Selenium ( WebScraping )  <br/>
        - Python    <br/>
          - numpy, pandas, matplotlib   <br/>
          - langdetect, langid, guess_language
      </p>
    </div>
  </div> -->


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
