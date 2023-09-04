
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum
from pyspark.sql.functions import split

# Read a dataset containing sales transactions. 
# Calculate the total sales amount for each product category using Spark's `groupBy` and aggregation functions.

spark = SparkSession.builder.appName("AverageScore").getOrCreate()

# READING CSV FILE WITH COLUMN SPARATOR ','
data = spark.read.options(delimeter=",").csv("sales.csv", header=True, inferSchema=True)

# CALCULATING TOTAL_SALES WITH GROUPBY AND AGGREGATION FUNCTION SUM
total_sales = data.groupBy("Category").agg(sum("Amount").alias("Total_Sales"))

total_sales.show()

spark.stop()

# OUTPUT:
# |   Category|Total_Sales|
# +-----------+-----------+
# |Electronics|        450|
# |   Clothing|        125|
# +-----------+-----------+


# 2. **Log Analysis:**
#    Analyze server log data to find the most frequently accessed URLs 
# and their corresponding IP addresses. Use Spark SQL to query and visualize the results.

spark = SparkSession.builder.appName("MostFrequently").getOrCreate()

#READING TEXT FILE
df = spark.read.text("server_log.txt")

#SPLITTING COLUMN VALUE INTO TWO COLUMNS: DATE AND URL_ADDRESS
df_spl = df.withColumn("date", split(df['value'], '/').getItem(0)) \
            .withColumn("url_address", split(df['value'], '/').getItem(1)) 

#SPLITTING NEWLY CREATED COLUMN URL_ADDRESS INTO TWO: URL_PAGE AND IP_ADDRESS        
df_spl2 = df_spl.withColumn("url_page", split(df_spl['url_address'], ' ').getItem(0)) \
            .withColumn("ip_address", split(df_spl['url_address'], ' ').getItem(1))
# df_spl2.show()

#cREATING TEMPORARY VIEW FOR SQL QUERIES
df_spl2.createOrReplaceTempView("most_frequently")

#PERFOMING SQL QUERY
results = spark.sql("SELECT url_page, ip_address, count(url_page) AS count FROM most_frequently GROUP BY url_page, ip_address")

results.show()

spark.stop()

# OUTPUT:
# +--------+-------------+-----+
# |url_page|   ip_address|count|
# +--------+-------------+-----+
# |   page1|192.168.1.102|    1|
# |   page2|192.168.1.101|    1|
# |   page2|192.168.1.103|    1|
# |   page3|192.168.1.100|    1|
# |   page1|192.168.1.100|    1|
# +--------+-------------+-----+

# Given a log file containing records of URLs accessed and 
# their corresponding timestamps, use MapReduce to count the number of times each URL was accessed.

spark = SparkSession.builder.appName("TextFile").getOrCreate()


def to_word_init(word):
    return (word, 1) #key: word, value: 1 -> word count starts with 1

def sum(a, b):
    return a + b    #function to sum word occurancy

def line_split(line):
    return line.split() #line split

text_rdd = spark.sparkContext.textFile("server_log.txt") # reading text file

count_rdd = (
    text_rdd.flatMap(line_split) # splitting lines in text file
    .filter(lambda word: word.startswith("/page"))  # looking for words that start with '/page'
    .map(to_word_init).reduceByKey(sum)     #summing the word occurancy
)

#opening text file to write the result

with open("URLCountRDD.txt", "w") as f:
    for (word,count) in count_rdd.collect():
        f.write(str((word,count))+"\n")

spark.stop()

# OUTPUT:
# ('/page1', 2)
# ('/page3', 1)
# ('/page2', 2)