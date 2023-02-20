import argparse
from catscore.db.mysql import MySQLConf
from pyspark import SparkConf, SparkContext, RDD
from pyspark.sql import SparkSession, DataFrame

parser = argparse.ArgumentParser(description="cats gmo")

# args params
parser = argparse.ArgumentParser(description='pyspark app args')
parser.add_argument('-ip', '--input_path', type=str, required=True, help='input folder path')
parser.add_argument('-db', '--db_conf', type=str, required=True, help='db conf path')
args = parser.parse_args()
print(f"args: {args}")

## db
mysql_conf = MySQLConf.from_json(args.db_conf)
print(f"mysql_conf {mysql_conf}")

# spark
conf = SparkConf()
conf.setAppName('spark_todb')
sc: SparkContext = SparkContext(conf=conf)
spark:SparkSession = SparkSession(sc)

df = spark.read.csv(path=f"{args.input_path}/*/*.csv", header=True)
df.show()
print(f"jdbc: {mysql_conf.connection_uri('jdbc')}")
df.write.jdbc(mysql_conf.connection_uri("jdbc"), table="raw_round_info", mode='overwrite')



      
