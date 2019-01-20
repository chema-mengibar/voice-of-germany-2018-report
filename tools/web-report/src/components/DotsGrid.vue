<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_dots-grid" ref="widget">
    <div v-bind:id="'info_' + pId" class="widget_dots-grid_info">{{info}}</div>
    <div class="filter"> 
      <p>X axis:  </p>
      <div id="sort_0" class="filter-option" v-bind:class="myBtnClass(null)" v-on:click="redraw(null)">Name</div>
      <div id="sort_1" class="filter-option" v-bind:class="myBtnClass('age')" v-on:click="redraw('age')">Age</div>
      <div id="sort_2" class="filter-option" v-bind:class="myBtnClass('gender')" v-on:click="redraw('gender')">Gender</div>
      <div id="sort_3" class="filter-option" v-bind:class="myBtnClass('buzzer_count')" v-on:click="redraw('buzzer_count')">Buzzers</div>
      <p class="separation">|</p>
      <p>Y axis:</p> 
      <p>Age</p>

    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import dataTools from '@/lib/dataTools.js';
import legendTools from '@/lib/legendTools.js';

export default {
  name: 'TimeLine',
  data(){
    return {
      pId: this.aId,
      pData: null,
      box:null,
      svg:null,
      divWidth:null,
      info: 'Click on the dots to display the participant data',
      selectedSortedKey:null
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
      dataTools.getData( _this.aSource )
        .then( (responseData )=> _this.pData = responseData );  
    } ,
    myBtnClass: function( _pSortKey ){
      return ( _pSortKey === this.selectedSortedKey )? 'selected-filter' : '';
    },
    redraw:function( _psortKey ){
      let svg = this.svg;
      this.info = '';
      this.selectedSortedKey = _psortKey;
      svg.selectAll("*").remove();
      this.drawWidget( this.pData, _psortKey )
    },
    drawWidget:function( pData, _sortKey=null ){
      var _this = this;
      var conf = {
        ageRanges: 4,
        maxAge: 64,
        legendsHeight: 30,
        barMargin: 5,
        paddingRow: 10,
        sortKey: _sortKey // null, 'age', 'gender', 'buzzer_count'
      };

      // pData = [ 
      //  { "gender": "female", "age": 48}, 
      // ]

      let margins = [ 2, 15, conf.legendsHeight, 2 ];
      let svg = this.svg
      let sc = {};
      sc.height = svg.attr( "height" );
      sc.width = svg.attr( "width" );
      sc.canvasHeight = svg.attr( "height" ) - margins[0] - margins[2];
      sc.canvasWidth = svg.attr( "width" ) - margins[1] - margins[3];

      var customPalette = {
        male: dataTools.customColorByName("menta"),
        female: dataTools.customColorByName("limon"),
      }
     

      // Init 
      var row = svg.selectAll("g").data( new Array( conf.ageRanges ) ).enter().append("g").attr('class','age-row')

      var barHeight = ( sc.canvasHeight - ( conf.barMargin * ( conf.ageRanges - 1 ) ) ) / conf.ageRanges   ;

      function rowPosition( _i ){
        return sc.canvasHeight - ( ( barHeight + conf.barMargin )  * _i  ) - barHeight + margins[0]
      }

      row.append('rect')
        .attr('class', (d,i)=> 'bar-age' )  
        .attr('width', (d,i)=> sc.canvasWidth + 'px' )
        .attr('height', (d,i)=> barHeight + 'px' )
        .attr('x', (d,i)=> margins[3] + 'px' )
        .attr('y', (d,i)=> rowPosition( i ) + 'px' )


      pData = pData.filter( (d)=>{ return ( d.age === parseInt( d.age, 10)) } )

      pData.sort(function(x, y){
        return d3.ascending(x[ conf.sortKey], y[  conf.sortKey ]);
      })
      
      var columnPx = (sc.canvasWidth - ( conf.paddingRow * 2) ) / (pData.length - 1);
      
      var step = Math.floor( conf.maxAge / conf.ageRanges );
      var rangeAgesList = Array.apply( null, Array( conf.ageRanges ) ).map( ( x, i )=> { 
        return  (i + 1) * step + 1; //corrector +1 for threesold range
      } );


      row.append('text')
        .attr('class', (d,i)=> 'label-age' )  
        .attr('x', (d,i)=> margins[3] + sc.canvasWidth + 2 +'px' )
        .attr('y', (d,i)=> rowPosition( i ) + 5 + 'px' )
        .text( (d,i)=> rangeAgesList[i] - 1 ) //corrector -1 label for threesold range


      var rangeRowList = Array.apply( null, Array( conf.ageRanges + 1 ) ).map( ( x, i )=>  i ) //  [ 0, 1, 2, 3, 4, 5, 6 ]

      let scaleYFct = d3.scaleThreshold().domain( rangeAgesList ).range( rangeRowList );

      let scaleYinRowFct = d3.scaleLinear().domain( [step,0] ).range( [0,barHeight] );

      function positionInRowByAge( _age ){
        if( _age > step ){
          var multiplo = Math.floor( _age / step );
          var f = ( _age - ( multiplo * step )  )
          return ( _age == ( multiplo * step ) ) ? scaleYinRowFct( step ) : scaleYinRowFct( f )
        }
        else{
          return scaleYinRowFct( _age )
        }
      }

      var circles = svg.append("g").attr('class','dots-layer')
        .selectAll("circle")
        .data( pData ).enter()
        .append("circle");

      circles
        .attr("cx", (d,i)=> margins[3] + conf.paddingRow +  ( columnPx * i ) + 'px')
        .attr("cy", (d,i)=> { 
          var rowId = scaleYFct( d.age );
          return rowPosition( rowId ) + positionInRowByAge( d.age )  + 'px'; //  
        } )
        .attr("r", (d,i)=> d.buzzer_count * 2 )
        .attr("fill", (d,i)=> customPalette[ d.gender ] )
        .on("click", (d, i)=>{
          var msg = `name: ${d.name} \n age: ${d.age}  \n buzzers: ${d.buzzer_count} `;
          circles
            .classed("selected", false)
            //.style("r", (e)=> e.buzzer_count * 2 );

          d3.select( d3.event.target )
            .classed("selected", true)
            //.style("r",5);
          _this.info = msg;
        });
      
      let legendData = [
        {key:"female", color: customPalette.female },
        {key:"male", color: customPalette.male },
      ];
      legendTools.horizontal( legendData, sc, svg, margins );
  
    }
  }
}
</script>
<style lang="scss">

@import '~@/assets/scss/main';

$widget--background-color: transparent; //#1f1f1f;

.widget{
  width:100%;
  height:100%;
  background: $widget--background-color;
}

.widget_dots-grid{
  position:relative;
  display:flex;
  //flex-direction: column-reverse;
  flex-flow: column-reverse wrap;
  justify-content: center;

  .label-age{
    font-size:8px;
    fill: $white;
  }

  .bar-age{
    fill: #0f0f0f;
  }

  .legend{
    text{
      fill: $white;
    }
  }

  svg{
    flex: 1 1 auto;
    circle{
      cursor:pointer;
      &.selected{
        stroke: rgba( 255,255,255,1);
        stroke-width:8px;
        stroke-dasharray:1;
      }

    }
  }

  .filter{
    display:flex;
    flex-direction:row;
    align-self: flex-start;
    height:30px;
  }

  .filter-option{
    margin-left:10px;
    background: $gris-m;
    padding: 2px 5px;
    border-radius: 12px;
    height:15px;
    line-height:12px;
    cursor: pointer;

    &.selected-filter{
      background: $electrico;
    }
  }

  p{
    margin-left:10px;
  }
  .widget_dots-grid_info{
    min-height:50px;
    margin:0 0 5px 2px;
    color:$white;
    white-space: pre-line;
    line-height:14px;
  }
}

</style>
