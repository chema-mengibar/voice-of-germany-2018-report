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


