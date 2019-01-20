var numSpaces = data.length - 1;
      sc.barMargin = 5;
      var realCanvas = sc.width - ( numSpaces * sc.barMargin);
      sc.barWidth = realCanvas / (data.length) ;
      sc.marginYLabelAndBar = 10;

      var bars = appendDataLayer( participantLikes );

      function appendDataLayer( iData ){
        // item = { date: N, likes: N}
        return svg.append("g").selectAll("rect").data( iData ).enter().append("rect")
          .attr("fill", function(d, i){   return '#ff4400';   } )
          .attr("x", function(d, i){  return  i * ( sc.barWidth + sc.barMargin );    } )
          .attr("y", function(d,i){   return ( sc.height - d3.format( intFormat )( convertLikes2Pixels( d.likes ) )  ) + 'px';   })
          .attr("height", function(d,i){  return d3.format( intFormat )( convertLikes2Pixels( d.likes ) )  + 'px';  })
          .attr("width", function(d,i){  return sc.barWidth + 'px';  });
      }
