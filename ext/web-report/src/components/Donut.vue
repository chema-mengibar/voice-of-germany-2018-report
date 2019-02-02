<template>
  <div  v-bind:id="'widget_' + pId" class="widget widget_donut" ref="widget"></div>
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
      if( this.box ){
        let windowPosY = window.pageYOffset;
        let windowHeight = window.innerHeight;
        let itemTop = this.box.node().getBoundingClientRect().top;

        if( itemTop < windowHeight-250 && itemTop >50 ){

          if( !_this.isAnimationReady ){
            _this.svg.selectAll("*").remove();
            _this.drawWidget( _this.pData );
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
      //Build svg in target div
      let box = d3.select( '#widget_' + _this.pId );
      _this.box = box;
      let boxWidth = box.node().getBoundingClientRect().width;
      let boxHeight = box.node().getBoundingClientRect().height;
      
      let w = boxWidth;
      let h = 350;

      _this.svg = box.append("svg")
        .attr("width", w )
        .attr("height", h)
        .attr("id","svg_" + _this.pId);
      //Get data, onchange the data will be rendered the widget
      dataTools.getData( '005-R_lang-quote.json' )
        .then( (responseData )=> _this.pData = responseData );  
    } ,
    drawWidget:function( pData ){

      let _this = this;
      let margins = [0, 0, 0, 10];
      let svg = this.svg
      let sc = {};
      sc.height = svg.attr( "height" );
      sc.width = svg.attr( "width" );
      sc.canvasHeight = svg.attr( "height" ) - margins[0] - margins[2];
      sc.canvasWidth = svg.attr( "width" ) - margins[1] - margins[3];
      /* lang_key, lang_quote, num_songs, total_songs */

      var donutWidth = 20; 
      var radius = Math.min( sc.width, 250) / 2;
      var rotation = 0;

      // var linearScale = d3.scaleLinear().domain([0,100]).range([0,100]);

      var customPalette = {
        de: dataTools.customColorByName("menta"),
        en: dataTools.customColorByName("electrico"),
        es: dataTools.customColorByName("limon"),
        it: dataTools.customColorByName("anyil"),
      }


      var arco = d3.arc().innerRadius(radius-7).outerRadius(radius);
      var arc = d3.arc().innerRadius(radius - donutWidth).outerRadius(radius);
      var pie = d3.pie().value(function(d) { return d.num_songs; }).sort(null);
      
      var svgContainer = svg.append("g").attr('transform', 'translate(' + (sc.width / 2) + ',' + (sc.height / 2) + ') rotate(' + rotation + ')');

      var g = svgContainer.selectAll("g").data( pie(pData) ).enter().append("g"); 

      var t = d3.transition()
        .duration(750)
        .ease(d3.easeLinear);

      var paths = g.append('path')
      .attr('d', arc)
      .attr('fill', function(d, i) {
        return dataTools.customColorByName('black');
      })
      .transition(t)
      .attr('d', arco)
      .attr('fill', function(d, i) {
        return customPalette[ pData[i].lang_key ];
      }); 



      function isOdd(num) { return num % 2;}

      var labels = g.append("text")
        .attr("transform", function(d, i) {
          var _d = arco.centroid(d);
          if( isOdd(i) ){  
            _d[0] *= 1.2;	_d[1] *= 1.2; 
          }
          else { 
            _d[0] *= 0.8;	_d[1] *= 0.8;
          }
          return 'translate(' + _d + ') rotate(-' + rotation + ')';
        })
        .attr("dy", ".50em")
        .style("text-anchor", "middle")
        .attr("class","donut-label")
        .text(function(d, i) {
          return pData[i].lang_quote + '%'
        })
        .attr('fill', function(d, i) {
          return customPalette[ pData[i].lang_key ];
         }); 

      function appendLegends( _legendData ){
       
        let gLegend = svg.append('g').attr('class','legend');
        
        let legendTop = 15;
        let legendLeft = margins[3];
        let legendItemWidth = 120;
        let legendItemHeight = 18;

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
          .style("fill", (d)=> d.color )  
      }

      let legendData =  [
        {key:"de", color: customPalette.de },
        {key:"en", color: customPalette.en },
        {key:"es", color: customPalette.es },
        {key:"it", color: customPalette.it },
      ];

      appendLegends( legendData );

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

.widget_donut{

  .donut-label{
    font-size:10px;
  }

  .legend{
    text{
      fill: $white;
    }
  }

}

</style>
