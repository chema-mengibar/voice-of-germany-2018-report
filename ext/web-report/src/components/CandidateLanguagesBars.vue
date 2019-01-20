<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_bars-candidate-lang" ref="widget"></div>
</template>

<script>
import * as d3 from 'd3';
import dataTools from '@/lib/dataTools.js';

export default {
  name: 'CandidateLanguagesBars',
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
        .attr("height", 350 )
        .attr("id","svg_" + _this.pId);

      dataTools.getData( _this.aSource )
        .then( (responseData )=> _this.pData = responseData );  
    },
    drawWidget:function( pData ){
      let svg = this.svg
      let margins = [5, 0, 0, 0]; //Clock
      let canvas = {
        oH: svg.attr( "height" ),
        oW: svg.attr( "width" ),
        iH: svg.attr( "height" ) - margins[0] - margins[2],
        iW: svg.attr( "width" ) - margins[1] - margins[3]
      };

      let config = {
        rowHeight: 15,
        labelWidth:50,
        fontSize: 10,
        cellWidth: 25,
      }

      var customPalette = {
        de: dataTools.customColorByName("menta"),
        en: dataTools.customColorByName("electrico"),
        es: dataTools.customColorByName("limon"),
        it: dataTools.customColorByName("anyil"),
      }

      let langBars = svg.append('g')
        .attr('class','lang-bars');
      
      let candidateRow = langBars.selectAll('g')
        .data( pData ).enter()
        .append('g')
          .attr('class','row_candidate')
          .attr('id', (d,i)=> 'row_candidate_' + i);
      
      candidateRow.append('text')
        .attr('class','row_label')
        .attr('x',(d,i)=> ( 10 ) + 'px' )
        .attr('y',(d,i)=> margins[0] + ( i * config.rowHeight ) + config.fontSize + 'px' )
        .style("text-anchor", "start")
        .text((d,i)=> i )
        

      for( let [kA, itemA] of Object.entries(pData) ){
        
        let langData = Object.keys( itemA.lang_counter ).map((kLang,i)=>{
          return { lang: kLang, count: itemA.lang_counter[ kLang ]  }
        });

        d3.select('#row_candidate_' + kA ).selectAll('rect')
          .data( langData ).enter()
          .append('rect')
            .attr('class','row_lang-block') 
            .attr('x', (d,i)=> ( config.labelWidth ) + (i* config.cellWidth) + 'px')
            .attr('y', (d,i)=> margins[0] + ( kA * config.rowHeight ) + 'px')
            .attr('width', (d,i)=> config.cellWidth + 'px')
            .attr('height', (d,i)=> (config.rowHeight - 5) + 'px')
            .attr('fill', (d,i)=> customPalette[ d.lang ] )
      }
    } 
  }
}
</script>
<style lang="scss">

@import '~@/assets/scss/main';

$widget--background-color: #060606;

.widget{
  width:100%;
  height:100%;
  background: $widget--background-color;
}

.widget_bars-candidate-lang{

  .row_label{
    fill:white;
    font-size:10px;
  }

}

</style>
