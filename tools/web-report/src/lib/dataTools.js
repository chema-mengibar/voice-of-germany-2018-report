var colors = {
  'rosado': '#bb4851',
  'carmin': '#F40C60',
  'ocre':   '#ECA345',
  'limon':  '#FEE043',
  'naranja':'#FF8500',
  'pistacho':'#A5D467',
  'menta':  '#17A360',
  'purpura':'#A96DAF',
  'lila':   '#AA34B7',
  'anyil':  '#6DC7FC',
  'cielo':  '#006ABA',
  'electrico' : '#2F39B1',
  'palette_01_a': '#222e50',
  'palette_01_b':'#007991',
  'palette_01_c':'#439a86',
  'palette_01_d':'#e9d985',
  'gris-t' : '#222222',
  'gris-m' : '#2F2F2F',
  'gris-c' : '#3E3E3E',
  'gris-b' : '#A3A099',
  'white' : '#ffffff',
  'black' : '#000000',
};


export default  {

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
    return jsonResp.json()

  },
  customColor:( idx )=>{ 
    return Object.values( colors )[idx];
  },
  customColors:( )=>{ 
    return Object.values( colors );
  },
  customColorByName:( _key )=>{ 
    return colors[ _key ];
  },

  getParticipantDatesInfos:( _participantData )=> {
    var isIn = true; 
    var dates = { 
      in: [],
      out: [],
      last: null
    }
    for( var dateRef in _participantData ){
      _participantData[ dateRef ].forEach( function( dateItem ) {
        if( dateItem.in === false ){
          isIn = false;
          dates.out.push( dateRef )
        }
        else{
          dates.in.push( dateRef )
        }
      })
    }

    let uniquesdataIn = dates.in.filter(function(elem, index, self) {
        return index == self.indexOf(elem);
    });

    let uniquesdataOut = dates.out.filter(function(elem, index, self) {
        return index == self.indexOf(elem);
    });

    dates.in = uniquesdataIn.sort();
    dates.out = uniquesdataOut.sort();
    
    dates.last = dates.out[0];
    return {'isIn': isIn, 'dates': dates};
  },
  getParticipantDayMaxLikes:( _dayKey, _participantData ) => {
    var dayRegister = _participantData[ _dayKey ];
    return Math.max.apply( Math, dayRegister.map(function(o) { return o.likes; } ) )
  },
  getMainMinMaxLikes:( pData, wantMin ) =>{
    var current = 0;
    for( var participantName in pData ){
      var participantData = pData[ participantName ];
      for( var dayKey in participantData ){
        var allInts = participantData[ dayKey ].map(function(o) { return o.likes; } );
        allInts.push( current  );
        current = (wantMin !== true) ?  Math.min.apply( Math, allInts ) :  Math.max.apply( Math, allInts );
      }
    }
    return current;
  },
  getMainDates:( pData ) =>{
    var current = [];
    for( var participantName in pData ){
      var participantData = pData[ participantName ];
      current.push.apply( current, Object.keys(participantData) )
    }
    let uniqueDates = current.filter(function(elem, index, self) {
        return index == self.indexOf(elem);
    });
    var uniqSortDates = uniqueDates.sort();
    return uniqSortDates;
  },


};


/*

let participantNames = Object.keys(data);

let participantName = participantNames[0];
let participantData =  data[ participantName ];
let participantDates = Object.keys( participantData );

let participantInfos = dataTools.getParticipantDatesInfos ( data[ participantName ] )
// console.log( participantName, participantInfos )

var dayKey =  participantInfos.dates.last;
var maxLikes = dataTools.getDayMaxLikes( dayKey, participantData )

var dayKey =  participantInfos.dates.in[0];
var maxLikes = dataTools.getDayMaxLikes( dayKey, participantData )

var outDatesLength = participantInfos.dates.out.length;
var dayKey =  participantInfos.dates.out[ outDatesLength - 1];
var maxLikes = dataTools.getDayMaxLikes( dayKey, participantData )    
console.log( maxLikes )

*/

/*
Format: http://bl.ocks.org/zanarmstrong/05c1e95bf7aa16c4768e

*/