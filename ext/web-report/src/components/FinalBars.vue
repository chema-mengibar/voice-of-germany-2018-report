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
      isVisible:false,
      isAnimationReady: false
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
  created(){ 
     window.addEventListener('scroll', this.handleScroll);
   },
  mounted(){
    let _this = this;
    setTimeout(function(){ 
      _this.divWidth = _this.getWidgetcontainerWidth();
      _this.initWidget();
    },100);
  
  },
  methods:{
     handleScroll (event) {
      let _this = this;
      if( _this.box ){

        let windowPosY = window.pageYOffset;
        let windowHeight = window.innerHeight;
        let itemTop = this.box.node().getBoundingClientRect().top;

        if( itemTop < windowHeight-250 && itemTop >50 ){
          
          if( !_this.isAnimationReady ){
            _this.svg.selectAll('*').remove();
            _this.drawWidget( this.pData );
          }
          _this.isVisible = true;
          _this.isAnimationReady = true;
        }

        if( itemTop > windowHeight || itemTop < 0 ){
          _this.isVisible = false;
          _this.isAnimationReady = false;
        }
      }
    },
    getWidgetcontainerWidth() {
      return this.$refs.widget.parentElement.clientWidth
    },
    initWidget:function(){
      let _this = this;

      let box = d3.select( '#widget_' + _this.pId );
      _this.box = box;
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
        barHeight: 20,
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

      //config.barWidth = (canvas.iW -(config.barMargin * (pData.length-1))) / pData.length ;
           
      var customPalette = [
        dataTools.customColorByName("naranja"),
        dataTools.customColorByName("lila"),
        dataTools.customColorByName("anyil"),
        dataTools.customColorByName("carmin"),
      ];

      var t = d3.transition()
        .duration(750)
        .ease(d3.easeLinear);

      let bars = svg.append('g')
        .attr('class','candidate-bar')
        .selectAll('g')
        .data( pData ).enter();
      
      
      let scaleXFct = d3.scaleLinear().domain( [0,maxQuote] ).range( [ margins[0], 150 ] );
      
      bars.append('rect')
        .attr('x', (d,i)=> margins[3] + 'px' )
        .attr('y', (d,i)=>  margins[0] + ( ( 30 + config.barMargin )* i) + 125 + 'px'  ) // label height = 100
        .attr('width', 0 + 'px'  )
        .attr('height', (d)=> config.barHeight + 'px' )
        .attr('fill',(d,i)=> customPalette[i] )
        .transition(t)
        .attr('width', (d,i)=>  margins[0] + scaleXFct( d.quote_final ) + 'px'  ) 
        
      
      bars.append('text')
        .attr('class', (d,i)=> 'column-label' )  
        .attr('x', (d,i)=> margins[3] + 'px' )
        .attr('y', (d,i)=>  margins[0] + ( ( 30 + config.barMargin )* i) + 125 + (config.barHeight/2) + 'px'  ) // label height = 100
        .text( (d,i)=> d.quote_final + ' %' )
        .attr('fill', (d,i)=> '#ffffff' )
        .transition(t)
        .attr('x', (d,i)=>  margins[3] + scaleXFct( d.quote_final + 15 )  + 'px' )
 

      svg.append('text')
        .attr('class', (d,i)=> 'bars-title-audience' )  
        .attr('x', (d,i)=> margins[3] + 'px' )
        .attr('y', (d,i)=>  margins[0] + 110 + 'px'  ) // label height = 100
        .text( 'Audience Votes' )


      let legendData = pData.map((d,i)=>{
        return { key: d.candidate_name, color: customPalette[i]  }
      })
      let _legendTop = 0;
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

  .bars-title-audience{
    fill:$white;
    font-size:16px;
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
