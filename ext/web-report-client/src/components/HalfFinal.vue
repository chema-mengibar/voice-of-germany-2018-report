<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_halffinal" ref="widget"></div>
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
      let space = 25;
      let coachDivision = ( sc.canvasWidth / 4 ) - space ;
      let coachRectHeight = 25;
      let scaleYFct =  d3.scaleLinear().domain( [0, 100] ).range( [0, sc.canvasHeight] );
      let scaleYpxFct =  d3.scaleLinear().domain( [sc.canvasHeight, 0] ).range( [0, sc.canvasHeight] );
      let customPalette = [
        dataTools.customColorByName('electrico'),
        dataTools.customColorByName('lila'),
        dataTools.customColorByName('carmin'),
        dataTools.customColorByName('menta'),
      ]

      let gBars = svg.append('g').attr('class','bars');
      svg.append('g').attr('class','bars').selectAll("rect").data( pData ).enter().append('rect')
        .attr('stroke', (d,i)=>{ 
          var color =  d3.color( customPalette[i] )
          return  color.darker( 1 ).rgb();
        }  )
        .attr('width', (d,i)=> coachDivision + 'px' )
        .attr('height', (d,i)=> coachRectHeight + 'px' )
        .attr('x', (d,i)=> margins[3] + ( (coachDivision + space) * i) + 'px' )
        .attr('y', (d,i)=> scaleYpxFct(coachRectHeight) + 'px' ) 

      svg.append('g').attr('class','coach-text').selectAll("text").data( pData ).enter().append('text')
        .style("text-anchor", "middle")
        .text((d,i)=> d.coach )
        .attr('x', (d,i)=> margins[3] + ( (coachDivision + space) * i) + ( coachDivision /2  ) + 'px' )
        .attr('y', (d,i)=> scaleYpxFct(coachRectHeight) + (coachRectHeight / 2) + 'px' )     

      function appendDataTeam( _teamIdx ){

        let participantDivision = ( coachDivision / 3 ) - 6;
        svg.append('g').attr('class','team').selectAll("rect").data( pData[ _teamIdx ]['participants'] ).enter().append('rect')
          .attr('class','participant')
          .attr('width', (d,i)=> participantDivision + 'px' )
          .attr('height', (d,i)=>  scaleYFct( d.quote ) + 'px' )
          .attr('x', (d,i)=> { 
            return margins[3] + ( ( coachDivision + space ) * _teamIdx) + ( ( (participantDivision + 5 )  * i) + 3 ) + 'px' } 
          )
          .attr('y', (d,i)=> { 
            return  sc.canvasHeight - coachRectHeight - scaleYFct( d.quote ) + 'px';
          } )
          .attr('fill', (d,i)=>{ 
            var isTeamWinner = ( d.name === pData[ _teamIdx ].winner.name );
            var colorD3 =  d3.color( customPalette[_teamIdx] )
            var color = isTeamWinner ? colorD3 : colorD3.darker( 5 ).rgb();
            return color;
          }  )  

        var n =  pData[ _teamIdx ]['participants'].length

        var posx = new Array( n ).fill( 0 );
        var posy = new Array( n ).fill( 0 );

        svg.append('g').attr('class','text1').selectAll("text").data( pData[ _teamIdx ]['participants'] ).enter().append('text')
          .attr('class','participant-text')
          .style("text-anchor", "start")
          .attr('x', (d,i)=> { 
            posx[ i ] = margins[3] + ( ( coachDivision + space ) * _teamIdx) + ( ( (participantDivision + 5 )  * i) + 3 ) +  (participantDivision/2);
            return posx[i] + 'px';
          })
          .attr('y', (d,i)=> { 
            posy[ i ] =  sc.canvasHeight - coachRectHeight - 10 - scaleYFct( d.quote );
            return posy[i]  + 'px';
          })
          .attr('fill', (d,i)=>{ 
            return customPalette[_teamIdx];
          }) 
          .attr("transform", function(d,i){
            var _x = posx[i];
            var _y = posy[i];
            return 'rotate(' + -90 + ' ' + _x + ',' +  _y + ')';
          })
          .text( (d,i)=>{ 
            return d.name;
          }  )    

        posx = new Array( n ).fill( 0 );
        posy = new Array( n ).fill( 0 );

        // participantDivision


        svg.append('g').attr('class','text2').selectAll("text").data( pData[ _teamIdx ]['participants'] ).enter().append('text')
          .attr('class','participant-quote')
          .style("text-anchor", "middle")
          .attr('x', (d,i)=> { 
            posx[ i ] = margins[3] + ( ( coachDivision + space ) * _teamIdx) + ( ( (participantDivision + 5 )  * i) + 3 ) +  (participantDivision/2);
            if( participantDivision < 20 ){
              posx[ i ] += 3;
            } 
            return posx[i] + 'px';
          })
          .attr('y', (d,i)=> { 
            posy[ i ] =  sc.canvasHeight - coachRectHeight - 12;
            if( participantDivision < 20 ){
              posy[ i ] -= 10;
            }  
            return posy[i]  + 'px';
          })
          .attr('fill', (d,i)=>{ 
            return dataTools.customColorByName('white');
          }) 
          .attr("transform", function(d,i){
            var _x = posx[i];
            var _y = posy[i];
            if( participantDivision < 20 ){
              return 'rotate(' + -90 + ' ' + _x + ',' +  _y + ')';
            }
            return '';
          })
          .text( (d,i)=>{ 
            return d.quote + ' %';
          }  )         
      }    
      appendDataTeam( 0 );
      appendDataTeam( 1 );
      appendDataTeam( 2 );
      appendDataTeam( 3 );
    }
  }
}
</script>
<style lang="scss">

@import '~@/assets/scss/main';

$widget--background-color: transparent; //#0f0f0f;

.widget{

}

.widget_halffinal{

  width:100%;
  height:100%;
  background: $widget--background-color;

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

  .coach-text{
  text{
   fill: $white;
  }
}

.participant-text{
  text{
    fill:white;
    font-family: Open Sans;
    font-size:12px;
  }
}

.base{
  fill: $gris-m;
}

}



</style>
