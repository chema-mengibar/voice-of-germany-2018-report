<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_dots-grid" ref="widget">
    <div v-bind:id="'info_' + pId" class="widget-dots-simple-grid_info">{{info}}</div>
    <div class="filter"> 
      <p>SORT BY:  </p>
      <div id="sort_0" class="filter-option option-color-0" v-bind:class="myBtnClass(null)" v-on:click="redraw(null)">Name</div>
      <div id="sort_1" class="filter-option option-color-1" v-bind:class="myBtnClass('age')" v-on:click="redraw('age')">Age</div>
      <div id="sort_2" class="filter-option option-color-2" v-bind:class="myBtnClass('gender')" v-on:click="redraw('gender')">Gender</div>
      <div id="sort_3" class="filter-option option-color-3" v-bind:class="myBtnClass('buzzer_count')" v-on:click="redraw('buzzer_count')">Buzzers</div>
     
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
      info: '',
      defaultInfo: 'Click on the dots to display the participant data',
      selectedSortedKey:null,
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
            
            _this.redraw( this.selectedSortedKey );
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
      this.info = this.defaultInfo;
      dataTools.getData( _this.aSource )
        .then( (responseData )=> _this.pData = responseData );  
    } ,
    myBtnClass: function( _pSortKey ){
      return ( _pSortKey === this.selectedSortedKey )? 'selected-filter' : '';
    },
    redraw:function( _psortKey ){
      let svg = this.svg;
      this.info = this.defaultInfo;
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

      let margins = [ 2, 40, conf.legendsHeight, 2 ];
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
        .attr('class', (d,i)=> 'simple-bar-age' )  
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
        .text( (d,i)=> rangeAgesList[i] - 1 + ' years' ) //corrector -1 label for threesold range


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

      var t = d3.transition()
            .duration(750)
            .ease(d3.easeLinear);

      var circles = svg.append("g").attr('class','dots-layer')
        .selectAll("circle")
        .data( pData ).enter()
        .append("circle");

      circles
        .attr("cx", (d,i)=> margins[3] + conf.paddingRow +  ( columnPx * i ) + 'px')
        .attr("cy", (d,i)=>{
           var rowId = scaleYFct( d.age );
          return rowPosition( rowId ) + positionInRowByAge( d.age )  + 'px'; //  
        } )
        .attr("r", (d,i)=> d.buzzer_count * 2 )
        .attr("fill", (d,i)=> 'transparent' )
        .on("click", (d, i)=>{
          var msg = `name: ${d.name} \n age: ${d.age}  \n buzzers: ${d.buzzer_count} `;
          circles
            .classed("selected", false)
            //.style("r", (e)=> e.buzzer_count * 2 );

          d3.select( d3.event.target )
            .classed("selected", true)
            //.style("r",5);
          _this.info = msg;
        })
        .transition(t)
        .attr("fill", (d,i)=> customPalette[ d.gender ] )


      
      let legendData = [
        {key:"female", color: customPalette.female },
        {key:"male", color: customPalette.male },
      ];
      legendTools.horizontal( legendData, sc, svg, margins );
     


      _this.svg.select('.legend').append('text')
        .style("font-size","10px")
        .attr("y", (d, i)=>( sc.canvasHeight + 20  + 'px') )
        .attr("x", (d,i )=> 120 + 'px' )
        .text(function(d) { return 'Buzzer Count'; })

      _this.svg.select('.legend')
        .selectAll(".buzzer-count").data( [1,2,3,4] ).enter().append('circle')
        .style("font-size","10px")
        .attr("cy", (d, i)=>( sc.canvasHeight + 18  + 'px') )
        .attr("cx", (d,i )=> 185 +  (d*(d*2)+d*3) + 'px' )
        .attr("r", (d)=> d*2 + 'px')
        .attr("class","buzzer-count")
        .style("stroke", '#ffffff' )  
        .style("stroke-width", '1px' ) 
        .style("fill", 'transparent' ) 
  
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

  .simple-bar-age{
    fill: #080808;
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
      &.option-color-0{   background: $carmin;   }
      &.option-color-1{   background: $lila;   }
      &.option-color-2{   background: $naranja;   }
      &.option-color-3{   background: $electrico;   }
    }
  }

  p{
    margin-left:10px;
  }
  .widget-dots-simple-grid_info{
    min-height:50px;
    max-width:280px;
    padding-left:10px;
    margin:0 0 5px 2px;
    background-color:$white;
    color:$black;
    white-space: pre-line;
    line-height:14px;
  }
}

</style>
