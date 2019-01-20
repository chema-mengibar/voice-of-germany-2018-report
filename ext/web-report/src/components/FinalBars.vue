<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_final-bars" ref="widget"></div>
</template>

<script>
import * as d3 from 'd3';
import dataTools from '@/lib/dataTools.js';
import legendTools from '@/lib/legendTools.js';

export default {
  name: 'FinalBars',
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
    "aId",
    "aSource"
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
      return this.$refs.widget.parentElement.clientWidth
    },
    initWidget:function(){
      let _this = this;

      let box = d3.select( '#widget_' + _this.pId );
      let boxWidth = box.node().getBoundingClientRect().width;
      let boxHeight = box.node().getBoundingClientRect().height;
      this.svg = box.append("svg")
        .attr("width", boxWidth )
        .attr("height", 275 )
        .attr("id","svg_" + _this.pId);

      dataTools.getData( _this.aSource )
        .then( (responseData )=> _this.pData = responseData );  
    },
    drawWidget:function( pData ){
      
      let svg = this.svg
      
      let quotes = pData.map((d,i)=>{
        return d.quote_final
      })
      const maxQuote = d3.max(quotes);
      const minQuote = d3.min(quotes);

      let config = {
        barMaxHeight: 150,
        legendsHeight: 30,
        barMargin:5,
      };

      let margins = [25, 10, 30, 10]; //Clock
    
      let canvas = {
        oH: svg.attr( "height" ),
        oW: svg.attr( "width" ),
        iH: svg.attr( "height" ) - margins[0] - margins[2],
        iW: svg.attr( "width" ) - margins[1] - margins[3]
      };

      config.barWidth = (canvas.iW -(config.barMargin * (pData.length-1))) / pData.length ;
           
      var customPalette = [
        dataTools.customColorByName("naranja"),
        dataTools.customColorByName("lila"),
        dataTools.customColorByName("anyil"),
        dataTools.customColorByName("carmin"),
      ];

      let bars = svg.append('g')
        .attr('class','candidate-bar')
        .selectAll('g')
        .data( pData ).enter();
      
      
      let scaleYFct = d3.scaleLinear().domain( [0,maxQuote] ).range( [ margins[0], config.barMaxHeight] );
      let scaleYFctReverse = d3.scaleLinear().domain( [maxQuote,0] ).range( [margins[0], config.barMaxHeight] );

      bars.append('rect')
        .attr('x', (d,i)=> margins[3] + ( ( config.barWidth + config.barMargin )* i) + 'px' )
        .attr('y', (d)=> scaleYFctReverse( d.quote_final ))
        .attr('width', (d)=> config.barWidth + 'px')
        .attr('height', (d)=> scaleYFct( d.quote_final ))
        .attr('fill',(d,i)=> customPalette[i] )
      
      bars.append('text')
        .attr('class', (d,i)=> 'column-label' )  
        .attr('x', (d,i)=> margins[3] + ( ( config.barWidth + config.barMargin )* i) + 2 + 'px' )
        .attr('y', (d,i)=>  scaleYFctReverse( d.quote_final ) - 5 )
        .text( (d,i)=> d.quote_final + ' %' )
        .attr('fill', (d,i)=> '#ffffff' )
     

      let legendData = pData.map((d,i)=>{
        return { key: d.candidate_name, color: customPalette[i]  }
      })
      let _legendTop = config.barMaxHeight + 25;
      legendTools.vertical( legendData, canvas, svg, margins, { legendTop: _legendTop + margins[0], legendLeft: margins[3] } );
   
    } 
  }
}
</script>
<style lang="scss">

@import '~@/assets/scss/main';

$widget--background-color: transparent; //#060606;

.widget_final-bars{
  width:100%;
  height:100%;
  background: $widget--background-color;

  .row_label{
    fill:white;
    font-size:9px;
  }
  .row_quote{
    fill:white;
    font-size:7px;
  }

  .legend{
    text{
      fill: $white;
      font-size:9px;
    }
  }

  .column-label{
    font-size:10px;
    font-weight: 400;
    text{
      fill: $white;
    }
  }


}

</style>
