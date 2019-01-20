define(function (require) {
    let Vue = require('vue');
    let moment = require('moment');
    let de = require('locale/de');

    require('./components/greeting');


    new Vue({
        el: '#main',
        data: {
            msg: '',
            participantMain: null,
            participantVs: null,
            inputDate: null,
            coachMain:null,
            coachVs:null,
            dayWeek: moment().format('d'),
            showDate: moment().format('YYYY.MM.DD'),
            //someDate: moment("20111031", "YYYYMMDD").fromNow() ,
        },
        methods: {
          sendValues: function ( ) {

            var _this = this;

            var sendData = {
              main: this.participantMain,
              vs: this.participantVs,
              dayweek: this.dayWeek,
              showdate: this.showDate
            }

            var sendRequest = fetch("http://motuo.info/tvog18/save.php",
            {
              method: 'POST',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
              body: JSON.stringify( sendData )
            })
            .then(function(res){ 
              return res.json();
            });

            sendRequest.then(function(data){ 
              console.log( data )
              _this.msg = 'Guardado!';
              _this.participantMain = null;
              _this.participantVs = null;
              _this.inputDate = null;
              _this.coachMain = null;
              _this.coachVs = null;

            },function( error ){ 
              console.log( error )
              _this.msg = 'No se ha podido guardar!';
            })
          },
          insertDate: function(  ){
            _date = this.inputDate;
            this.dayWeek = moment( _date, "DD.MM.YYYY").format('d');
            this.showDate =  moment( _date, "DD.MM.YYYY").format('YYYY.MM.DD');

          },
          getParticipants: function( coachType ){
         
            return teams[ this[coachType] ];
          },
          getCoaches: function(){
            return [
              { 'name': "Michael Patrick" },
              { 'name': "Mark" },
              { 'name': "Michi & Smudo" },
              { 'name': "Yvonne" }
            ];
          },
         
        },
        created: function () {
            moment.locale('de');
        },
        template: `
        <div class="container app">
          <div class="row app__row">

            <div class="col-sm app__col__salutation">
              <p> TVOG18 Performance register</p>
              <i class="p__salutation">{{msg}}</i>
             
            </div>

            <div class="col-sm app__col blank">
              <p class="p__title">Participant: {{participantMain}}</p>

              <select v-model="coachMain">
                <option v-for="thing in getCoaches()" v-bind:value="thing.name" @>{{ thing.name }}</option>
              </select>

              <input v-model="participantMain" placeholder="Escribe aqui">
              <select v-model="participantMain">
                <option v-for="thing in getParticipants('coachMain')" v-bind:value="thing.name" @>{{ thing.name }}</option>
              </select>
            </div>

            <div class="col-sm app__col blank">
              <p class="p__title">Participant VS: {{participantVs}}</p>

              <select v-model="coachVs">
                <option v-for="thing in getCoaches()" v-bind:value="thing.name" @>{{ thing.name }}</option>
              </select>

              <input v-model="participantVs" placeholder="Escribe aqui">
              <select v-model="participantVs">
                <option v-for="thing in getParticipants('coachVs')" v-bind:value="thing.name" @>{{ thing.name }}</option>
              </select>
            </div>

            <div class="col-sm app__col blank">
              <p class="p__title">Fecha:</p>   <input v-model="inputDate" v-on:change="insertDate" placeholder="Insert Date DD.MM.YYYY">
              <p class="p__text">Date:{{ showDate }}</p>
              <p class="p__text">Day week: {{ dayWeek }}</p>

            </div>

            <div class="col-sm app__col col__button">
              <button class="app__button" v-on:click="sendValues()"> Guardar  </button>
            </div>

          </div>
        </div>
        `,
    });
});


// <greeting :greet="msg" to="World"></greeting>


/*
Issues:
https://stackoverflow.com/questions/21624503/load-external-scripts-with-requirejs-without-access-to-config

Libs:
https://momentjs.com/docs/
*/
