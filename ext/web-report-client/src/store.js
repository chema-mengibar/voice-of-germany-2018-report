import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isHomeInited:false,
    text:{},
  },
  mutations: {
    setHomeInited( state, flag ){
      this.state.isHomeInited = flag;      
    },
    setText( state, text ){
      this.state.text = text;      
    },
   
  },
  actions: {

  }
})
