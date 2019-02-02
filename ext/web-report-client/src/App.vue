<template>
<div id="app" class="wrapper">

  <ul class="app__main-nav">
    <li class="app__nav-item" v-for="route in [{title:'/home',name:'Report'},{title:'/about_project', name:'Process'}]">
      <router-link :to="route.title" class="nav-link" active-class="active">
          {{ route.name }}
      </router-link>
    </li>
  </ul>

  <div class="container" v-if="!inited">
     <div class="row row--underlined" >
      </div>
    <div class="row  row__text--centered row--underlined" >
      <div class="block">
        <font-awesome-icon class="app__spinner" icon="circle-notch" spin/>
      </div>
    </div>
  </div> 

  <router-view/>
</div>
</template>

<script>

import { library } from '@fortawesome/fontawesome-svg-core'
import { faCircleNotch } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faCircleNotch )

export default {
  components:{
    FontAwesomeIcon
  },
  computed: {
    inited () {
      return this.$store.state.isHomeInited; 
    }
  },
}
</script>


<style lang="scss">
 @import '~@/assets/scss/main';
 
 .app__main-nav{
   list-style-type: none;
    text-align: right;
    width:100%;
    height:30px;
 }

 .app__nav-item{
    text-decoration: none;
    font-size:12px;
    display:inline;

    &:first-of-type{
      margin-right: 12px;
    }

    a {
    color: $white;
    
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

.app__spinner{
  font-size:28px;
}


</style>
