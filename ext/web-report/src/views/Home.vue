<template>
<div class="container">

  <!-- <div class="row row--underlined" >
    <div class="block">
      <h1>TVOG18 <br/> FINALE REPORT</h1>
    </div>
    <div class="deco-header" style="display:none"></div>
  </div> -->

  <!-- <div class="row row__text--centered">
    <div class="block">
      <h4>Lorem ipsum temporavit</h4>
      <p>
        Nullam accumsan elit et sapien tempor consectetur. Sed volutpat tortor sapien, interdum iaculis mi tempor a. Integer commodo leo risus, id imperdiet quam facilisis a.
      </p>
    </div>
  </div> -->

  <!-- <div class="row row__1a1">
    <div class="block">
      <TimeLine :aId="'01'"></Timeline>
    </div>
  </div> -->

  <!-- <div class="row row__1a1">
    <div class="block">
      <HalfFinal :aId="'02'"></HalfFinal>
    </div>
  </div> -->

  <!-- <div class="row row__1a1">
    <div class="block">
      <Donut :aId="'03'"></Donut>
    </div>
    <div class="block">
      <BarsTopten :aId="'04'" :aSource="'005-R_top-ten-artists.json'"></BarsTopten>
    </div>

    <div class="block">
      <BarsTopten :aId="'05'" :aSource="'005-R_top-ten-artists-de.json'"></BarsTopten>
    </div>
  </div> -->

  
  <!-- <div class="row row__1a1">
    <div class="block">
      <DotsGrid :aId="'06'" :aSource="'006-R_all-participants_1.0.json'"></DotsGrid>
    </div>
  </div> -->

  <!-- <div class="row row__1a1">
    <div class="block">
      <DotsGridCoaches :aId="'07'" :aSource="'006-R_all-participants_1.0.json'"></DotsGridCoaches>
    </div>
  </div> -->

   <!-- <div class="row row__1a1">
    <div class="block">
      <TableBuzzers :aId="'08'" :aSource="'009_blinds-extended_1.0.json'"></TableBuzzers>
    </div>
  </div> -->
  
<!-- 
  <div class="row row__1a1">
    <div class="block">
      <TableCoach :aId="'09'" :aSource="'009_blinds-extended_1.0.json'"></TableCoach>
    </div>
  </div>
   -->


  <div class="row row__1a1">
    <div class="block">
      <CandidateLanguagesBars :aId="'09'" :aSource="'011-R.00_songs-lang_1.0.json'"></CandidateLanguagesBars>
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
  }
}
</script>

<style lang="sass">
@import '~@/assets/scss/main';

</style>
