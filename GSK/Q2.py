import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, regexp_extract
from pyspark.sql.functions import to_timestamp

spark = SparkSession.builder \
    .master("local") \
    .appName("Spark application") \
    .getOrCreate()

path = r"sample.log"

df = spark.read.json(path)

split_df = df.select(regexp_extract('value', r'^(.*)\s+(\w+)\s+(:..\w+:)\s+(\w+.*)', 1).alias('timestamp')
                        ,regexp_extract('value', r'^(.*)\s+(\w+)\s+(:..\w+:)\s+(\w+.*)', 2).alias('level')
                        ,regexp_extract('value', r'^(.*)\s+(\w+)\s+(:..\w+:)\s+(\w+.*)', 3).alias('object')
                        ,regexp_extract('value', r'^(.*)\s+(\w+)\s+(:..\w+:)\s+(\w+.*)', 4).alias('text')
                        )

log_df = split_df.select(to_timestamp(split_df.timestamp, 'MM/yy HH:mm:ss').alias('Date'),'level','object','text')
log_df.show(truncate=False)