Python Help


#### objToJson
```py
with open( outputFullPathFile  + '.json' , 'w') as outfile:
  json.dump( jsonData , outfile , indent=2)
```

#### jsonToDf
```py
with open( inputFullPathFile ) as train_file:
  dictTrain = json.load(train_file)

dfN = pd.DataFrame.from_dict(dictTrain, orient='index')
dfN.reset_index(level=0, inplace=True)
```

#### dfToJsonObj
```py
df_as_json = DF.to_dict(orient='split')
return df_as_json
```

#### dfToCsv
```py
DF.to_csv( path_or_buf = outputFullPathFile + '.csv' , sep=",", quoting=None, index=False )
```

#### csvToDF
```py
pd.read_csv( filepath_or_buffer = inputFullPathFile , sep=",", quoting= 3 )
```
