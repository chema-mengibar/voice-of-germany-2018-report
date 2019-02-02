**Languages detect**  
https://stackoverflow.com/questions/39142778/python-how-to-determine-the-language
https://es.wikipedia.org/wiki/ISO_639-1


**Name detect**  
https://thetokenizer.com/2013/08/25/how-to-easily-recognize-peoples-names-in-a-text/


**JS Loops**  
https://stackoverflow.com/questions/14379274/how-to-iterate-over-a-javascript-object
https://developer.mozilla.org/es/docs/Web/JavaScript/Referencia/Sentencias/for...of

**Fontawesome in Vue**  

```
// import { library } from '@fortawesome/fontawesome-svg-core'
// import { faCoffee  } from '@fortawesome/free-solid-svg-icons'
// import { fasGithub } from '@fortawesome/fontawesome-free'
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
```


#Python Issues


#### List iteration
The Iterator [1:] return a list

```
list = ['a','b']
lettersGroup1 = list[0]
lettersGroup2 = list[1]
>> a
>> b
```
```
list = ['a','b']
lettersGroup1 = list[0]
lettersGroup2 = list[1:]
>> a
>> [b]
```


#### Wrong characters in Regexp
The song title was copied with "*" characters, and this causes an error in the regexp pattern

**string:** @niggas@@in@@paris@
**wrong regexp:** (?:@ni**as@)|(?:@in@)|(?:@paris@)
**right regexp:** (?:@ni\*\*as@)|(?:@in@)|(?:@paris@)
