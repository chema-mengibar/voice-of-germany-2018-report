<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_bars-candidate-lang" ref="widget"></div>
</template>

<script>
import * as d3 from 'd3';
import dataTools from '@/lib/dataTools.js';
import legendTools from '@/lib/legendTools.js';

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
        .attr("height", 200 )
        .attr("id","svg_" + _this.pId);

      dataTools.getData( _this.aSource )
        .then( (responseData )=> _this.pData = responseData );  
    },
    drawWidget:function( pData ){
      
      let numCandidates = pData.length;
      const SONG_BY_CANDIDATE = ( numCandidates == 4) ? 7: 4 ;
      const MODE = ( numCandidates == 4) ? 'final': 'semifinal' ;
      let svg = this.svg

      let config = {
        rowHeight: 15,
        labelWidth:95,
        fontSize: 10,
        cellWidth: 25,
        cellMargin:2,
        legendsHeight: 30,
      };
      let margins = [25, 0, 30, 10]; //Clock

      //resize the svg height with the number of data-rows
      svg.attr('height', ()=>{
        return ( pData.length * config.rowHeight ) + margins[0] + margins[2];
      });
      
      let canvas = {
        oH: svg.attr( "height" ),
        oW: svg.attr( "width" ),
        iH: svg.attr( "height" ) - margins[0] - margins[2],
        iW: svg.attr( "width" ) - margins[1] - margins[3]
      };

      let resizeCell = (canvas.iW - config.labelWidth - 50) / SONG_BY_CANDIDATE;
      config.cellWidth = resizeCell;
 
      //legends parameter to legends.tool
      canvas.canvasHeight = canvas.oH - config.legendsHeight;
     
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
          .attr('id', (d,i)=> 'wid_' + this.pId + '_row_candidate_' + i);
      
      // Label in row
      candidateRow.append('text')
        .attr('class',(d,i)=>{
          let className = 'row_label';
          if( MODE == 'final' ){
            className += d.is_finalist_winner ? ' is-winner' : '';
          }
          else{
            className += d.is_semifinalist_winner ? ' is-winner' : '';
          }
          return className;
        })
        .attr('x',(d,i)=> ( config.labelWidth - 10 ) + 'px' )
        .attr('y',(d,i)=> margins[0] + ( i * config.rowHeight ) + config.fontSize + 'px' )
        .style("text-anchor", "end")
        .text((d,i)=> d.candidate_name )
        
      // Songs-cells in row
      for( let [kA, itemA] of Object.entries(pData) ){

        let langsLog = []
        for( let langItem of itemA.lang_counter ) {
          let tempKeyList = Array( langItem._value ).fill( langItem._key )
          langsLog = [...langsLog, ...tempKeyList]
        };

        d3.select('#wid_' + this.pId + '_row_candidate_' + kA ).selectAll('rect')
          .data( langsLog ).enter()
          .append('rect')
            .attr('class','row_lang-block') 
            .attr('x', (d,i)=> ( config.labelWidth ) + ( i * (config.cellWidth + config.cellMargin) )  + 'px')
            .attr('y', (d,i)=> margins[0] + ( kA * config.rowHeight ) + 'px')
            .attr('width', (d,i)=> config.cellWidth + 'px')
            .attr('height', (d,i)=> (config.rowHeight - 5) + 'px')
            .attr('fill', (d,i)=> customPalette[ d ] )
      }

      // Quote in row
      candidateRow.append('text')
        .attr('class',(d,i)=>{
          let className = 'row_quote';
          if( MODE == 'final' ){
            className += d.is_finalist_winner ? ' is-winner' : '';
          }
          else{
            className += d.is_semifinalist_winner ? ' is-winner' : '';
          }
          return className;
        })
        .attr('x',(d,i)=> ( config.labelWidth + ( (config.cellWidth + config.cellMargin ) * d.num_songs ) ) + 5 + 'px' )
        .attr('y',(d,i)=> margins[0] + ( i * config.rowHeight ) + config.fontSize + 'px' )
        .style("text-anchor", "start")
        .text((d,i)=>{
          if( MODE == 'final' ){
            return d.quote_final + '%';
          }
          else{
            return d.quote_semifinal  + '%';
          }
        })

      // Color legends
      let legendData = [
        {key:"de", color: customPalette.de },
        {key:"en", color: customPalette.en },
        {key:"winner", color: dataTools.customColorByName("naranja") },
      ];
      legendTools.horizontal( legendData, canvas, svg, margins );

      //Columns legend
      let columnLegend = svg.append('g')
        .attr('class','legend-column');

      columnLegend.append('text')
        .attr('class','legend-column_name')
        .style("text-anchor", "end")
        .attr('x',()=> ( config.labelWidth - 10 )  + 'px')
        .attr('y',()=> 15 + 'px')
        .text('Name')
      
      columnLegend.append('text')
        .attr('class','legend-column_name')
        .style("text-anchor", "start")
        .attr('x',()=> ( config.labelWidth )  + 'px')
        .attr('y',()=> 15 + 'px')
        .text('Songs')
      
      columnLegend.append('text')
        .attr('class','legend-column_name')
        .style("text-anchor", "start")
        .attr('x',()=> ( config.labelWidth + ( ( config.cellWidth + config.cellMargin ) * SONG_BY_CANDIDATE ) ) + 5 + 'px')
        .attr('y',()=> 15 + 'px')
        .text('Users Vote')

    } 
  }
}
</script>
<style lang="scss">

@import '~@/assets/scss/main';

$widget--background-color: transparent;//#060606;

.widget{
  width:100%;
  height:100%;
  background: $widget--background-color;
}

.widget_bars-candidate-lang{

  .row_label{
    fill:white;
    font-size:9px;
    &.is-winner{
      fill: $naranja;
    }
  }
  .row_quote{
    fill:white;
    font-size:7px;
    &.is-winner{
      fill: $naranja;
    }
  }

  .legend{
    text{
      fill: $white;
      font-size:9px;
    }
  }

  .legend-column_name{
    fill:$white;
    font-size:8px;
  }

}

</style>
