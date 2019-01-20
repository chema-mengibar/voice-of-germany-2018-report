export default  {
  
  horizontal: ( _legendData, sc, svg, margins, _conf={} ) => {

    var gLegend = svg.append('g').attr('class','legend');

    var legendTop = sc.canvasHeight + 20;
    var legendLeft = margins[3];
    var legendItemWidth = 50;

    gLegend
      .selectAll("text").data( _legendData ).enter().append('text')
      .style("font-size","10px")
      .attr("y", (d, i)=>( legendTop  + 'px') )
      .attr("x", (d,i )=> legendLeft + ( legendItemWidth * i) + 11 + 'px' )
      .text(function(d) { return d.key; })
    
    gLegend
      .selectAll("circle").data( _legendData ).enter().append('circle')
      .attr("cy", (d,i)=>( legendTop - 3 + 'px')  )
      .attr("cx", (d, i )=> legendLeft + ( legendItemWidth * i) + 6 + 'px' )
      .attr("r","3px")
      .style("fill", (d)=> d.color )  
  },

  vertical: ( _legendDate, sc, svg, margins, _conf={} ) =>{


  }

}