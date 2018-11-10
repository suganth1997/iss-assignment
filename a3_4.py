#application_1524406905265_3229 on small dataset
#application_1524406905265_3277 on full dataset
from pyspark import SparkContext, SparkConf
 
sc = SparkContext.getOrCreate()

def parse_with_commas(x):
	if x.count(',')>2:
		return [x[:x.find(',')], x[x.find(',')+1:x.rfind(',')], x[x.rfind(',')+1:]]
	else:
		return x.split(',')

movies = sc.textFile("hdfs:///user/simmhan/ml/small/movies.csv").cache()
rdd_movies = movies.map(parse_with_commas).filter(lambda z:z[0] != 'movieId').map(lambda x:len(x[2].split('|')))
max_num_genres = rdd_movies.max(key=int)
print('Maximum genre given to a single movie = ' + str(max_num_genres))