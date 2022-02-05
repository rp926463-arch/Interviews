#------------------------------------------------------------------------------------
#   PROCESS JSON FILE USING PYTHON                                                  |
#                                                                                   |
#   e.g.file records                                                                |
#       {"name": "Gilbert", "wins": [["straight", "7♣"], ["one pair", "10♥"]]}      |
#       {"name": "Alexa", "wins": [["two pair", "4♠"], ["two pair", "9♠"]]}         |
#       {"name": "May", "wins": []}                                                 |
#       {"name": "Deloise", "wins": [["three of a kind", "5♣"]]}                    |
#------------------------------------------------------------------------------------
#

path = r"sample.json"

import json
import re
import pandas as pd

iotmsg_data ="""\
{   
"data": [%s]
}
"""
with open(path) as fr:
    lines = fr.read().splitlines()
fr.close()

with open("cache.json", "w") as fw:
    for line in lines:
        fw.write(line + ",\n")

fw.close()
 
f = open("cache.json")
d = f.read() 
f.close()

d = d[:-2]
st = re.sub(r"[\s+]", "", iotmsg_data) % (d)
dict = json.loads(st)

df = pd.DataFrame()

for i in dict['data']:
    df = df.append(i, ignore_index = True)
df = df.explode('wins')
print(df.head(6))
#print(df.to_dict('list'))
#print(df.to_dict('records'))


#------------------------------------------------------------------------------------
#   PROCESS JSON FILE USING PYSPARK                                                 |
#                                                                                   |
#   e.g.file records                                                                |
#       {"name": "Gilbert", "wins": [["straight", "7♣"], ["one pair", "10♥"]]}      |
#       {"name": "Alexa", "wins": [["two pair", "4♠"], ["two pair", "9♠"]]}         |
#       {"name": "May", "wins": []}                                                 |
#       {"name": "Deloise", "wins": [["three of a kind", "5♣"]]}                    |
#------------------------------------------------------------------------------------
'''
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode

spark = SparkSession.builder \
    .master("local") \
    .appName("Spark application") \
    .getOrCreate()

df = spark.read.json(path)

df.select(df.name, explode(df.wins)).show(truncate=False)

spark.stop()
'''
