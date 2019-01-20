import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    selectedPanel: 12,
    panelsData:[],
    isMenuOpen:false 
  },
  mutations: {
    setMenuOpen( state ){
      this.state.isMenuOpen = !state.isMenuOpen;      
    },
    setPanelsData( panels ){
      this.state.panelsData = panels;      
    },
    setSelectedPanel( iPanel ){
      this.state.selectedPanel = iPanel;      
    }
  },
  actions: {

  }
})
