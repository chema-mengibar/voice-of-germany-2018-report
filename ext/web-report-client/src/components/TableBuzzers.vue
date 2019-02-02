<template>
  <div v-bind:id="'widget_' + pId" class="widget widget_table-buzzers" ref="widget">
    <svg  v-bind:id="'svg_' + pId" v-if="dataLoaded" v-bind:width="svgSettings.width" v-bind:height="svgSettings.height">
      <g class="svg-canvas">
        <g class="auditions-grid-colum" v-for="(candidate, index_col) in pData.candidates_data" :key="index_col">
          <g class="auditions-grid-row" v-for="(coach, index_row) in pData.coaches_keys" :key="index_row">
            <rect class="auditions-cell" v-bind='cell(index_col, index_row)' ></rect>
          </g>     
        </g>
      </g>
      <g class="svg-legends">
        <g class="svg-legend" v-bind='legendPosition(index_coach)' v-for="(coach, index_coach) in pData.coaches_keys" :key="index_coach">
          <circle class="legend-circle" v-bind='legendCircle(index_coach)' ></circle>
          <text class="legend-text" v-bind='legendText(index_coach)' >{{coach}}</text>
        </g>
      </g>
    </svg>
  </div>
</template>

<script>
import * as d3 from 'd3';
import dataTools from '@/lib/dataTools.js';


export default {
  name: 'TableBuzzers',
  data(){
    return {
      pId: this.aId,
      pData: null,
      box:null,
      svg:null,
      dataLoaded:false,
      svgSettings:{
        height:0,
        width:0,
        margins : [0, 10, 0, 10],
        customPalette:[],
        colors:{},
        heightCell:8,
      }
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
      this.dataLoaded = true;
      this.drawWidget( dataValue ) ;
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

      let box = d3.select( '#widget_' + _this.pId );
      _this.svg = box.select('svg');
      _this.svgSettings.width = box.node().getBoundingClientRect().width;
      _this.svgSettings.height = 90; // box.node().getBoundingClientRect().height;

      dataTools.getData(  _this.aSource  )
        .then( (responseData )=> _this.pData = responseData );  
    } ,
    drawWidget:function( pData ){
      
      let _this = this;
      let svg =  _this.svg
            
      var customPalette = [ 
        dataTools.customColorByName("menta"),
        dataTools.customColorByName("electrico"),
        dataTools.customColorByName("limon"),
        dataTools.customColorByName("anyil"),
      ];
    
      _this.svgSettings.customPalette = customPalette;
      _this.svgSettings.colors['cell'] = dataTools.customColorByName("gris-t");

    },
    svgCanvas: function( ){
      let _this = this;
      let H = _this.svgSettings.height, W = _this.svgSettings.width;
      return {
        H: H,
        W: W,
        h : H - _this.svgSettings.margins[0] - _this.svgSettings.margins[2],
        w : W - _this.svgSettings.margins[1] - _this.svgSettings.margins[3]
      };
    },
    cell:function( _col, _row ){
      let _this = this;
      var canvas = _this.svgCanvas();
      var _data =_this.pData;

      var widthCell =  canvas.w / _this.pData.candidates_data.length  ; // _this.svgSettings.cellWidth,
      var heightCell =  _this.svgSettings.heightCell;

      var cellColor = _this.svgSettings.colors.cell;

      var candidate_buzzers = _data.candidates_data[_col].buzzer_coaches_names
      if( _data.candidates_data[_col].buzzer_count > 0 ){
        if(  _data.candidates_data[_col].buzzer_coaches_names.indexOf( _data.coaches_keys[_row] ) > -1 ){
          cellColor = _this.svgSettings.customPalette[ _row ];
        }
      }
      return {
        x: _this.svgSettings.margins[3] + (_col * widthCell),
        y:_row *  ( heightCell +1 ),
        width: widthCell,
        height: heightCell,
        fill: cellColor,
      };
    },   
    legendPosition:function(_idx){
      let _this = this;
      var _data =_this.pData;
      //var pos = (_data.coaches_keys[_idx].length * 7) * _idx;
      var posX = 0 * _idx;
      var posY = 12 * _idx;
      return {
        transform: 'translate(' + posX + ',' + posY + ')',
      }
    },
    legendCircle:function( _idx ){
      let _this = this;
      var _data =_this.pData;
      var cellColor =  _this.svgSettings.customPalette[ _idx ];
      var r = 3;
      return {
        cx: _this.svgSettings.margins[3] + r,
        cy: ( _this.svgSettings.heightCell * _data.coaches_keys.length ) + 15,
        r: r,
        fill: cellColor,
      };
    },
    legendText:function( _idx ){
      let _this = this;
      var _data =_this.pData;
      return {
        x: _this.svgSettings.margins[3] + 12,
        y: ( _this.svgSettings.heightCell * _data.coaches_keys.length ) + 18,
        fill: 'white',
      };
    },
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

.widget_table-buzzers{

  .legend-text{
    font-size:8px;
  }

}

</style>
