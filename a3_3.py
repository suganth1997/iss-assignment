#application_1524406905265_3227 on small dataset
#application_1524406905265_3281 on full dataset
from pyspark import SparkContext, SparkConf

sc = SparkContext.getOrCreate()
ratings = sc.textFile("hdfs:///user/simmhan/ml/small/ratings.csv").cache()
rdd_ratings = ratings.map(lambda x:x.split(',')).filter(lambda z:z[0] != 'userId').map(lambda y:float(y[2])).sortBy(lambda z:z).zipWithIndex().map(lambda x:(x[1], x[0]))
median_rating = rdd_ratings.lookup(rdd_ratings.count()/2)
print('Median Value of ratings = ' + str(median_rating))