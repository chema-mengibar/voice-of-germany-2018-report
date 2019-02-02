<template>
<div class="container" v-if="inited">

  <div class="row row--underlined" >
    <div class="block">
      <h1>TVOG18 <br/> FINALE REPORT</h1>
    </div>
    <div class="deco-header" style="display:none"></div>
  </div>

  <div class="row row__text--centered row--underlined row_pb-40"  >
    <div class="block">
      <h3>{{text.text_intro_title}}</h3>
      <p>{{text.text_intro_body}}</p>
    </div>
  </div>


  <!-- ########################### PARTICIPANT  ######################################################-->
  <div class="row">
    <div class="block">
      <h2>{{text.participants_title}}</h2>
      <p>{{text.participants_body}} </p>
    </div>
  </div>
  <div class="row row__1a1">
    <div class="block">
      <DotsGrid :aId="'06'" :aSource="'006-R_all-participants_1.0.json'"></DotsGrid>
    </div>
  </div>

  <!-- ########################### COACHES ######################################################-->
  <div class="row">
    <div class="block">
      <h2>{{text.coaches_title}}</h2>
      <p>{{text.coaches_body}} </p>
    </div>
  </div>

  <div class="row row--with-graf">
    <div class="block">
      <h3>{{text.buzzers_title}}</h3>
      <p>{{text.buzzers_body}} </p>
    </div>
  </div>
  <div class="row row__1a1 row--with-text">
    <div class="block">
      <TableBuzzers :aId="'08'" :aSource="'009_blinds-extended_1.0.json'"></TableBuzzers>
    </div>
  </div>

  <div class="row row--with-graf">
    <div class="block">
      <h3>{{text.participants_choose_title}}</h3>
      <p>{{text.participants_choose_body}}</p>
    </div>
  </div>
  <div class="row row__1a1 row--with-text">
    <div class="block">
      <TableCoach :aId="'09'" :aSource="'009_blinds-extended_1.0.json'"></TableCoach>
    </div>
  </div>
  
  <div class="row row--with-graf">
    <div class="block">
      <h3>{{text.coach_choose_title}}</h3>
      <p>{{text.coach_choose_body}}</p>
    </div>
  </div>
  <div class="row row__1a1">
    <div class="block">
      <DotsGridCoaches :aId="'07'" :aSource="'006-R_all-participants_1.0.json'"></DotsGridCoaches>
    </div>
  </div>

  <!-- ########################### SONGS ######################################################-->
  <div class="row">
    <div class="block">
      <h2>{{text.songs_title}}</h2>
      <p>{{text.songs_body}}</p>
    </div>
  </div>

  <div class="row row__1a1 row--underlined">
    <div class="block">
      <Donut :aId="'03'"></Donut>
    </div>
    <div class="block">
      <BarsTopten :aId="'04'" :aSource="'005-R_top-ten-artists.json'"></BarsTopten>
    </div>

    <div class="block">
      <BarsTopten :aId="'05'" :aSource="'005-R_top-ten-artists-de.json'"></BarsTopten>
    </div>
  </div>


  <!-- ########################### HALF-FINAL ######################################################-->

  <div class="row row__text--centered">
    <div class="block">
      <h2>{{text.half_final_title}}</h2>
      <p>{{text.half_final_body}} </p>
    </div>
  </div>

  <div class="row row__text--centered row--with-graf">
    <div class="block">
      <h3>{{text.user_likes_title}}</h3>
      <p>{{text.user_likes_body}} </p>
    </div>
  </div>
  <div class="row row__1a1 row--underlined">
    <div class="block">
      <HalfFinal :aId="'02'"></HalfFinal>
    </div>
  </div>

  <!-- ########################### FINAL ######################################################-->

  <div class="row">
    <div class="block">
      <h2>{{text.finalist_title}}</h2>
    </div>
  </div>

  <div class="row row__1a1">
    <div class="block">
      <p>{{text.finalist_body}}</p>
    </div>
  </div>

  <div class="row row__2a1">
    <div class="block">
      <TimeLine :aId="'01'"></Timeline>
    </div>
     <div class="block">
      <FinalBars :aId="'50'" :aSource="'011-R.01_songs-votes__final_1.0.json'"></FinalBars>
    </div>
  </div>

  <div class="row row--with-graf">
    <div class="block">
      <h3>{{text.facts_title}}</h3>
      <p>{{text.facts_body}}</p>
    </div>
  </div>
  <div class="row row__1a1 row--underlined">
    <div class="block">
      <CandidateLanguagesBars :aId="'100'" :aSource="'011-R.00_songs-lang__show-semifinal_1.0.json'"></CandidateLanguagesBars>
    </div>
    <div class="block">
      <CandidateLanguagesBars :aId="'101'" :aSource="'011-R.00_songs-lang__show-final_1.0.json'"></CandidateLanguagesBars>
    </div>
  </div>

  <!-- ########################### BYE ######################################################-->


  <div class="row row__text--centered row--underlined">
    <div class="block">
      <h2>{{text.bye_title}}</h2>
      <p>{{text.bye_body}}</p>

      <p class="feature"> <a v-bind:href="text.github" target="_blank"> <i class="fab fa-github"></i> Github   </a> </p>
      <p class="feature"> <a v-bind:href="text.twitter" target="_blank">   <i class="fab fa-twitter"></i> Twitter</a> </p>
     
    </div>
  </div>



  
</div>

</template>

<script>
import TimeLine  from '@/components/TimeLine.vue';
import HalfFinal  from '@/components/HalfFinal.vue';
import Donut  from '@/components/Donut.vue';
import BarsTopten  from '@/components/BarsTopten.vue';
import DotsGrid  from '@/components/DotsGrid.vue';
import DotsGridCoaches  from '@/components/DotsGridCoaches.vue';
import TableBuzzers  from '@/components/TableBuzzers.vue';
import TableCoach  from '@/components/TableCoach.vue';
import CandidateLanguagesBars  from '@/components/CandidateLanguagesBars.vue';
import FinalBars  from '@/components/FinalBars.vue';

import dataTools from '@/lib/dataTools.js';

import { fab } from '@fortawesome/fontawesome-free/js/all'

export default {
  name: 'home',
  components: {
    TimeLine,
    Donut,
    HalfFinal,
    BarsTopten,
    DotsGrid,
    DotsGridCoaches,
    TableBuzzers,
    TableCoach,
    CandidateLanguagesBars,
    FinalBars, 
  },
  watch: {
    text( dataValue ) {
      this.$store.commit('setHomeInited', true )
    },
  },
  data(){
    return{
      text:{}
    }
  },
  mounted(){
    if( !this.inited ){
      this.getText();
    }
    else{
      this.text = this.$store.state.text;
    }
  }, 
  computed: {
    inited () {
      return this.$store.state.isHomeInited; 
    }
  },
  methods:{
    getText:function(){
      let _this = this;
      dataTools.getData( 'text.json' )
        .then( ( responseData )=>{
           this.$store.commit('setText', responseData ) 
          return  _this.text = responseData
         } );  
    }

  }
}
</script>

<style lang="scss">
@import '~@/assets/scss/main';



.feature{
  margin-top:20px;
  display:block;
  
  a {
    color: $white;
    font-size:18px;
    text-decoration: none;
    //margin-left:20px;

    &:visited {
      color: $white;
    }
    &:hover {
      color: $white;   
    }
    &:active {
      color: $white;
    }
  }

}


</style>
