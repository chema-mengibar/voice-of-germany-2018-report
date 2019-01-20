<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_timeline" ref="widget"></div>
</template>

<script>

import * as d3 from 'd3';
import dataTools from '@/lib/dataTools.js';

//
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
  created(){
   // nothing to do here
  },
  mounted(){
    let _this = this;
    setTimeout(function(){ 
      _this.divWidth = _this.getWidgetcontainerWidth();
      _this.initWidget();
    },100);
  
  },
  methods:{
    async getData( fileName ) {

      var _this = this;

      var sendData = {
        cmd:'data',
        file: fileName,
      }

      let req = await fetch("http://motuo.info/web-report-server/reporter.php",
      {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        mode: 'cors',
        cache: 'no-cache',
        body: JSON.stringify( sendData )
      })

      let jsonResp = await req;
      let data =  await jsonResp.json()
      this.pData = data;

    },
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
      this.getData( 'timeline-weblikes_1.2.json' );  
  
    } ,
    drawWidget:function( pData ){
      
      let margins = [0, 10, 40, 10];

      let svg = this.svg
      let sc = {};
      sc.height = svg.attr( "height" );
      sc.width = svg.attr( "width" );
      sc.canvasHeight = svg.attr( "height" ) - margins[0] - margins[2];
      sc.canvasWidth = svg.attr( "width" ) - margins[1] - margins[3];
      
      // Prepare Data
      let participantNames = Object.keys( pData );

      // Y
      var mainMinLikes = dataTools.getMainMinMaxLikes( pData );
      var mainMaxLikes = dataTools.getMainMinMaxLikes( pData, true );
      let scaleYFct = d3.scaleLinear().domain([mainMaxLikes, mainMinLikes]).range( [margins[0], (sc.canvasHeight + margins[0])]);
                
      // X 
      let mainDates = dataTools.getMainDates( pData );
      let scaleXFct =  d3.scaleLinear().domain([0, (mainDates.length - 1)]).range([margins[3], (sc.canvasWidth + margins[3])]);

      function getParticipantData( _participantName ){
        let participantData =  pData[ _participantName ];
        let participantInfos = dataTools.getParticipantDatesInfos ( pData[ _participantName ] )
        //console.log( _participantName, participantInfos )

        return participantInfos.dates.in.map( function( inDateKey ){
          var likes = dataTools.getParticipantDayMaxLikes( inDateKey, participantData );
          var idx = mainDates.indexOf( inDateKey );
          return {
            date: inDateKey,
            likes: likes,
            idx: idx,
            x: parseFloat( scaleXFct( idx )),
            y: parseFloat( scaleYFct( likes ))
          }
        } )
      }

      // Build SVG
      function appendParticipantLine( _participantLikes, _params ){
        let line = d3.line()
          .x(function(d) { return d['x']; })
          .y(function(d) { return d['y']; });
        let path = svg.append('path')
          .attr('d', line( _participantLikes ))
          .attr( 'stroke', ( ) => dataTools.customColorByName( _params.color ) );
      }


      function appendLegends( _legendData ){
       
        let gLegend = svg.append('g').attr('class','legend');
        
        let legendTop = 15;
        let legendLeft = margins[3];
        let legendItemWidth = 120;
        let legendItemHeight = 25;

        let cursorX = margins[3] + legendLeft;

        gLegend
          .selectAll("text").data( _legendData ).enter().append('text')
          .style("font-size","10px")
          .attr("y", (d, i)=>( legendTop + ( legendItemHeight * i) + 'px') )
          .attr("x", ()=> legendLeft + 10 + 'px' )
          .text(function(d) { return d.key; })
        
        cursorX = margins[3] + legendLeft;
        gLegend
          .selectAll("circle").data( _legendData ).enter().append('circle')
          .attr("cy", (d,i)=>( legendTop - 2 + ( legendItemHeight * i) + 'px')  )
          .attr("cx", ()=> legendLeft )
          .attr("r","5px")
          .style("fill", (d)=> dataTools.customColorByName( d.color) )  
      }

      let legendData =  [
        {key:"Benjamin Dolic", color:"naranja"},
        {key:"Eros Atomus Isler", color:"anyil"},
        {key:"Samuel R\u00f6sch", color:"limon"},
        {key:"Jessica Schaffler", color:"menta"},
      ];

      appendLegends( legendData );
      
      
      let data01 = getParticipantData( 'Eros Atomus Isler' );
      appendParticipantLine( data01, { color: 'anyil' } );
      
      let data02 = getParticipantData( 'Benjamin Dolic' );
      appendParticipantLine( data02, { color: 'naranja' } );
      
      let data03 = getParticipantData( 'Jessica Schaffler' );
      appendParticipantLine( data03, { color: 'menta' } );
      
      let data04 = getParticipantData( 'Samuel R\u00f6sch' );
      appendParticipantLine( data04, { color: 'limon' } );


      var x_axis = d3.axisBottom().scale(scaleXFct).tickFormat((d, i) =>  mainDates[d].substring(5) )
      var y_axis = d3.axisLeft().scale(scaleYFct).tickFormat((d, i) =>  d )

      svg.append("g").attr("class", "timeline__axis timeline__axis__x")
       .attr("transform", "translate(0," + sc.canvasHeight + ")")
        .call( x_axis )

      svg.append("g").attr("class", "timeline__axis timeline__axis__y")
        .attr("transform", "translate("+ ( sc.width - margins[1] ) + ",0)")
        .call( y_axis )  
        // .selectAll("text").attr("y", 0).attr("x", 9).attr("dy", ".35em")
        //   .attr("transform", "rotate(45)").style("text-anchor", "start");;
 

    }
  }
  
}
</script>

<style lang="scss">
@import '~@/assets/scss/main';

$widget--background-color: transparent; // #0f0f0f;

.widget{
  width:100%;
  height:100%;
  background: $widget--background-color;
}

.widget_timeline{

  path {
    fill: none;
    stroke-width: 3px;
  }

  .timeline__axis{
    color: $gris-c;
    &__x{
      font-size: 8px;
    }

    path {
      fill: none;
      stroke-width: 1px;
    }
  }

  .legend{
    text{
      fill: $white;
    }
  }

}

</style>
