#application_1524406905265_3222 on small dataset
#application_1524406905265_3282 on full dataset
from pyspark import SparkContext, SparkConf
 
sc = SparkContext.getOrCreate()
ratings = sc.textFile("hdfs:///user/simmhan/ml/small/ratings.csv").cache()
rdd_ratings = ratings.map(lambda x:x.split(',')).filter(lambda z:z[0] != 'userId')
avg_num_of_ratings = rdd_ratings.map(lambda y:(int(y[0]), 1)).groupByKey().mapValues(sum).map(lambda z:z[1]).mean()
avg_val_of_ratings = rdd_ratings.map(lambda y:int(y[2])).mean()

print('Average Number of Ratings by Users' + str(avg_num_of_ratings) + '\n' + 'Average Value of Ratings' + str(avg_val_of_ratings))
