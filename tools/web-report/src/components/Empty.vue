<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_empty" ref="widget"></div>
</template>

<script>
import * as d3 from 'd3';
import dataTools from '@/lib/dataTools.js';

export default {
  name: 'TimeLine',
  data(){
    return {
      pId: this.aId,
      pData: null,
      box:null,
      svg:null,
      divWidth:null,
    }
  },
  props:[
    "aId"
  ],
  watch: {
    aId(value) {
      this.pId = value;
    },
    pData( dataValue ) {
      this.drawWidget( dataValue ) 
    },
  },  
  created(){  },
  mounted(){
    let _this = this;
    setTimeout(function(){ 
      _this.divWidth = _this.getWidgetcontainerWidth();
      _this.initWidget();
    },100);
  
  },
  methods:{
    getWidgetcontainerWidth() {
      // return  this.$refs.widget.clientWidth;
      return this.$refs.widget.parentElement.clientWidth
    },
    initWidget:function(){
      let _this = this;
      //Build svg in target div
      let box = d3.select( '#widget_' + _this.pId );
      let boxWidth = box.node().getBoundingClientRect().width;
      let boxHeight = box.node().getBoundingClientRect().height;
      
      let w = boxWidth; //this.divWidth; //- m[1] - m[3];
      let h = 350; //boxHeight; //- m[0] - m[2];

      this.svg = box.append("svg")
        .attr("width", w )
        .attr("height", h)
        .attr("id","svg_" + _this.pId);
      //Get data, onchange the data will be rendered the widget
      dataTools.getData( 'half-final-quotes_1.1.json' )
        .then( (responseData )=> _this.pData = responseData );  
    } ,
    drawWidget:function( pData ){
      let margins = [0, 10, 0, 10];
      let svg = this.svg
      let sc = {};
      sc.height = svg.attr( "height" );
      sc.width = svg.attr( "width" );
      sc.canvasHeight = svg.attr( "height" ) - margins[0] - margins[2];
      sc.canvasWidth = svg.attr( "width" ) - margins[1] - margins[3];


    }
  }
}
</script>
<style lang="scss">

@import '~@/assets/scss/main';

$widget--background-color: transparent; //#0f0f0f;

.widget{
  width:100%;
  height:100%;
  background: $widget--background-color;
}

</style>
