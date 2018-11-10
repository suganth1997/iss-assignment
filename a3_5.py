#application_1524406905265_3230 on small dataset
#application_1524406905265_3279 on full dataset
from pyspark import SparkContext, SparkConf

sc = SparkContext.getOrCreate()

def parse_with_commas(x):
	if x.count(',')>2:
		return [x[:x.find(',')], x[x.find(',')+1:x.rfind(',')], x[x.rfind(',')+1:]]
	else:
		return x.split(',')

movies = sc.textFile("hdfs:///user/simmhan/ml/small/movies.csv").cache()
rdd_movies = movies.map(parse_with_commas).filter(lambda z:z[0] != 'movieId').flatMap(lambda x:x[2].split('|')).filter(lambda y:y != '(no genres listed)')
rdd_genres_kv_pair = rdd_movies.map(lambda x:(x,1)).groupByKey().mapValues(sum)
max_genre = rdd_genres_kv_pair.max(key = lambda x:x[1])[0]
min_genre = rdd_genres_kv_pair.min(key = lambda x:x[1])[0]