from pyspark.sql.functions import explode
from pyspark.sql.types import *
from pyspark.sql.functions import col


def dummy_function(data_str):
    return [i.split(':') for i in data_str.split(';')]

#read file to DF
df = spark.read.csv("/mnt/Sales/Sales/sample.txt", sep='|',header=True,inferSchema=True)

#register UDF
dummy_function_udf = udf(dummy_function, ArrayType(ArrayType(StringType())))

#convert value to 2D list by calling UDF
newdf = df.withColumn("value", dummy_function_udf(df['value']))

#explode list
df = newdf.select(newdf.id, explode(newdf.value).alias('value'))

#extract values
data = df.select("id", df.value[0], df.value[1])

#rename columns
df = data.select(col("id"), col("value[0]").alias("key"), col("value[1]").alias("value"))
df.show()

#Write to CSV
df.coalesce(1).write.format("csv").option("header", True).option("sep",",").mode("overwrite").save("/mnt/Sales/Sales/output.csv")