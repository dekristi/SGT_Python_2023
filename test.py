from itertools import count

# def prime_num():
#     a=1
#     while True:
#        if a == 1:
#           a += 1
#        else:
#           for c in count(a+1):
#             for i in range(2, c):
#                 if c % i == 0:
#                    break
#                 else:
#                     yield c
#             a += 1

# result = prime_num()

# next(result)

# next(result)

# def prime_num():
#     a = 0
#     while True:
#         if a < 2:
#             a == 2
#         else:
#             if all(a%i!=0 for i in range(2,a)):
#                 yield a   
#             a += 1

# result = prime_num()

# print(next(result))

# next(result)
# next(result)
# next(result)
# next(result)
# next(result)

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import split
from functools import reduce

spark = SparkSession.builder.appName("TextFile").getOrCreate()

# df = spark.read.text("server_log.txt")

# df_spl = df.withColumn("date", split(df['value'], '/').getItem(0)) \
#             .withColumn("url_address", split(df['value'], '/').getItem(1)) 
            
# df_spl2 = df_spl.withColumn("url_page", split(df_spl['url_address'], ' ').getItem(0)) \
#             .withColumn("ip_address", split(df_spl['url_address'], ' ').getItem(1))
# # df_spl2.show()

# df_spl2.createOrReplaceTempView("most_frequently")

# results = spark.sql("SELECT url_page, ip_address, count(url_page) AS count FROM most_frequently GROUP BY url_page, ip_address")

# results.show()

# spark.stop()

def sum(a, b):
    return a + b

def to_word_init(word):
    return (word, 1)

def line_split(line):
    return line.split()

text_rdd = spark.sparkContext.textFile("server_log.txt")

count_rdd = (
    text_rdd.flatMap(line_split)
    .filter(lambda word: word.startswith("/page"))
    .map(to_word_init).reduceByKey(sum)
)

with open("URLCountRDD.txt", "w") as f:
    for (word,count) in count_rdd.collect():
        f.write(str((word,count))+"\n")



# def count(characters):
#     return reduce(reducer, map(lambda char: dict([[char, 1]]), characters))
    
# def reducer(i, j):
#     for k in j: i[k] = i.get(k, 0) + j.get(k, 0)
#     return i

# print(count('testing yeah it works'))



