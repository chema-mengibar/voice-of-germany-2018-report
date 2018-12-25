# Import Export in Python

## Requeriments
```
import sys
import os
from os.path import isfile, join
import urllib, json
import pandas as pd
import csv
```

### Obj to Json-File
```
with open( outputFullPathFile  + '.json' , 'w') as outfile:
    json.dump( jsonData , outfile , indent=2)
```

### Json-File to Dataframe
```
with open( inputFullPathFile ) as train_file:
    dictTrain = json.load(train_file)
dfN = pd.DataFrame.from_dict(dictTrain, orient='index')
dfN.reset_index(level=0, inplace=True)
```

### Dataframe to Json Object
```
  df_as_json = DF.to_dict(orient='split')
```

### Dataframe to CSV-File
```
DF.to_csv( path_or_buf = outputFullPathFile + '.csv' , sep=",", quoting=None, index=False )
```

### CSV-File to Dataframe
```
pd.read_csv( filepath_or_buffer = inputFullPathFile , sep=",", quoting= 3 )
```
