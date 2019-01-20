// loadTools.js

// https://stackoverflow.com/questions/39109789/what-limitations-apply-to-opaque-responses 


//module.exports = {

export default  {
    
    fetchAsync: async ( libUrl ) => {
        
        // await response of fetch call
        let response = await fetch( libUrl );
        // only proceed once promise is resolved
        let data = await response.json();
        // only proceed once second promise is resolved
        return data;
     },

   
    fetchAsyncMD: async ( libUrl, token ) => {

        //console.log( token )

        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Authorization", "Bearer " + token);

        var miInit = {
            method: 'GET',
            headers: {
                'Authorization': "Bearer " + token,
                'content-type': 'application/json'
              },
              mode: 'cors'
            //headers: myHeaders,
            //cache: 'no-cache',
            //mode:"no-cors"
        };
        let response = await fetch( libUrl, miInit );
        let data = await response;
        //console.log( data )
        return data.json();
    },



    token: async ( longTerm ) => {

        var libUrl = 'https://api.heroku.com/oauth/authorizations';
        var myHeaders = new Headers();
        myHeaders.append("Authorization", "Bearer " + longTerm );
        myHeaders.append("Content-Type", "application/json");
        myHeaders.append("Accept", "application/vnd.heroku+json; version=3");
        
        var miInit = { 
            method: 'POST',
            headers: myHeaders,
            mode: 'cors',
            cache: 'no-cache',
            body:''
        };
        let response = await fetch( libUrl, miInit );
        let data = await response;
        return data.json();
    },

    obj2obj:( iObj )=> {

        let oObj = JSON.parse(JSON.stringify(iObj));
        return oObj;
    }
};




  