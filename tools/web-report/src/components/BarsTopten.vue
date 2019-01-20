<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_bars-topten" ref="widget"></div>
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
      //Build svg in target div
      let box = d3.select( '#widget_' + _this.pId );
      let boxWidth = box.node().getBoundingClientRect().width;
      let boxHeight = box.node().getBoundingClientRect().height;
      
      let w = boxWidth;
      let h = 350;

      this.svg = box.append("svg")
        .attr("width", w )
        .attr("height", h)
        .attr("id","svg_" + _this.pId);
      //Get data, onchange the data will be rendered the widget
      dataTools.getData( _this.aSource )
        .then( (responseData )=> _this.pData = responseData );  
    } ,
    drawWidget:function( pData ){

      let margins = [0, 5, 0, 10];
      let svg = this.svg
      let sc = {};
      sc.height = svg.attr( "height" );
      sc.width = svg.attr( "width" );
      sc.canvasHeight = svg.attr( "height" ) - margins[0] - margins[2];
      sc.canvasWidth = svg.attr( "width" ) - margins[1] - margins[3];
      /* lang_key, lang_quote, num_songs, total_songs */

     var columnNames = pData.columns;
     var listData = pData.data;

     var customPalette = {
      de: dataTools.customColorByName("menta"),
      en: dataTools.customColorByName("electrico"),
      es: dataTools.customColorByName("limon"),
      it: dataTools.customColorByName("anyil"),
     }

    var globs = { 
      deezer_playlist_id : 0,
      song : 1,
      artist : 2,
      year : 3,
      genre : 4,
      deezer_quote : 5,
      lang : 6
    }

    var row = svg.selectAll("g").data( listData ).enter().append("g").attr('class','song-row')
    var barHeight = 15;
    var labelHeight = 18;

    var scaleDimension = 0.1
    var listQuotes = listData.map( ( d )=> d[ globs.deezer_quote ]  );
    var maxQuote = d3.max( listQuotes )
    var minQuote = d3.min( listQuotes ) - scaleDimension;

    var quoteLabelWidth = 50;

    // scaleLog Issue zeros: https://stackoverflow.com/questions/40438911/logarithmic-scale-returns-nan
    let scaleXFct =  d3.scaleLinear().domain( [ minQuote , maxQuote] ).range( [0, sc.canvasWidth - margins[1] - quoteLabelWidth ] );

    row.append('rect')
      .attr('class', (d,i)=> 'bar-song--' + d[ globs.lang ] )  
      .attr('d-singer', (d,i)=> d[ globs.artist ] )  
      .attr('width', (d,i)=> scaleXFct( d[ globs.deezer_quote ] ) + 'px' )
      .attr('height', (d,i)=> barHeight + 'px' )
      .attr('x', (d,i)=> margins[3] + 'px' )
      .attr('y', (d,i)=> margins[0] + ( ( barHeight + labelHeight ) * i  ) + labelHeight + 'px' )
      .attr('fill', (d,i)=>{ 
        var songLang = d[ globs.lang ];
        return customPalette[ songLang ];
      } )  

    row.append('text')
      .attr('class', 'label-row' )  
      .attr('x', (d,i)=> margins[3] + scaleXFct( d[ globs.deezer_quote ] ) + 5 + 'px' )
      .attr('y', (d,i)=> margins[0] + ( ( barHeight + labelHeight ) * i  ) + ((barHeight/1.5) + labelHeight ) + 'px' )
      .style("text-anchor", "start")
     .text( (d, i) => d[ globs.deezer_quote ] ) 
     .attr('fill', (d,i)=>{ 
        var songLang = d[ globs.lang ];
        return customPalette[ songLang ];
      } )  

    row.append('text')
      .attr('class', 'label-row label-row--artist' )  
      .attr('x', (d,i)=> margins[3] + 'px' )
      .attr('y', (d,i)=> margins[0] + ( ( barHeight + labelHeight ) * i  )  - 2 + labelHeight + 'px' )
      .style("text-anchor", "start")
     .text( (d, i) => d[ globs.artist ] + ': ' + d[ globs.song ] ) 
    }
  }
}
</script>
<style lang="scss">

@import '~@/assets/scss/main';

$widget--background-color: transparent; //#060606;

.widget{
  width:100%;
  height:100%;
  background: $widget--background-color;
}

.widget_bars-topten{

  .label-row{
    font-size: 8px;

    &--artist{
      fill:$white;
    }
  }

  .legend{
    text{
      fill: $white;
    }
  }

}

</style>
