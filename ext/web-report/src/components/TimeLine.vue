<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_timeline" ref="widget"></div>
</template>

<script>

import * as d3 from 'd3';
import dataTools from '@/lib/dataTools.js';
import legendTools from '@/lib/legendTools.js';

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
      isVisible:false,
      isAnimationReady: false
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
    async getData( fileName ) {

      var _this = this;

      var sendData = {
        cmd:'data',
        file: fileName,
      }

      let req = await fetch("http://motuo.info/tvog18/reporter.php",
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
       _this.box = box;
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
          .y(function(d) { return d['y']; })

        let path = svg.append('path')
          .attr('d', line( _participantLikes ))
          .attr( 'stroke', ( ) => {
            return _params.color
          })
          ;
      }



      var customPalette = [
        dataTools.customColorByName("naranja"),
        dataTools.customColorByName("lila"),
        dataTools.customColorByName("anyil"),
        dataTools.customColorByName("carmin"),
      ];
      
      let legendData =  [
        {key:"Benjamin Dolic", color: customPalette[2] },
        {key:"Eros Atomus Isler", color:customPalette[3] },
        {key:"Samuel R\u00f6sch", color: customPalette[0] },
        {key:"Jessica Schaffler", color: customPalette[1] },
      ];

      // sc.iH = sc.canvasHeight;
      // legendTools.vertical( legendData, sc, svg, margins, { legendTop: 25, legendLeft: margins[3] } );
           
      
      let data01 = getParticipantData( 'Eros Atomus Isler' );
      appendParticipantLine( data01, legendData[1] );
      
      let data02 = getParticipantData( 'Benjamin Dolic' );
      appendParticipantLine( data02, legendData[0] );
      
      let data03 = getParticipantData( 'Jessica Schaffler' );
      appendParticipantLine( data03, legendData[3] );
      
      let data04 = getParticipantData( 'Samuel R\u00f6sch' );
      appendParticipantLine( data04, legendData[2] );

      var t = d3.transition()
        .duration(1200)
        .ease(d3.easeLinear);

       svg.append('rect')
        .attr('x', (d,i)=> 0 + 'px' )
        .attr('y', (d,i)=>  '0'  ) // label height = 100
        .attr('width', '100%'  )
        .attr('height', '100%'  )
        .attr('fill', '#000000' )
        .transition(t)
        .attr('x', (d,i)=> '100%' )


      var x_axis = d3.axisBottom().scale(scaleXFct).tickFormat((d, i) =>  mainDates[d].substring(5) )
      var y_axis = d3.axisLeft().scale(scaleYFct).tickFormat((d, i) =>  d )

      svg.append("g").attr("class", "timeline__axis timeline__axis__x")
       .attr("transform", "translate(0," + sc.canvasHeight + ")")
        .call( x_axis )

      svg.append("g").attr("class", "timeline__axis timeline__axis__y")
        .attr("transform", "translate("+ ( sc.width - margins[1] ) + ",0)")
        .call( y_axis )  

      svg.append('text')
        .attr('class', (d,i)=> 'bars-title-audience' )  
        .attr('x', (d,i)=> margins[3] + 'px' )
        .attr('y', (d,i)=>  margins[0] + 25 + 'px'  ) 
        .text( 'Official Website likes' )  


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

  .bars-title-audience{
    fill:$white;
    font-size:16px;
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
