#application_1524406905265_3231 on small dataset
#application_1524406905265_3278 on full dataset
from pyspark import SparkContext, SparkConf
from itertools import combinations
sc = SparkContext.getOrCreate()
def parse_with_commas(x):
	if x.count(',')>2:
		return [x[:x.find(',')], x[x.find(',')+1:x.rfind(',')], x[x.rfind(',')+1:]]
	else:
		return x.split(',')

movies = sc.textFile("hdfs:///user/simmhan/ml/small/movies.csv").cache()
rdd_genre_pairs = movies.map(parse_with_commas).filter(lambda z:z[0] != 'movieId').filter(lambda y: y[2].find('|')!=-1).flatMap(lambda x:list(combinations(x[2].split('|'),2)))
genre_kv_pair = rdd_genre_pairs.map(lambda x:(x,1)).groupByKey().mapValues(sum)
most_likely_genre_pair = genre_kv_pair.max(key = lambda x:x[1])[0]
least_likely_genre_pair = genre_kv_pair.min(key = lambda x:x[1])[0]
print('The most likely pair of genres to occur are ' + most_likely_genre_pair[0] + ' and ' + most_likely_genre_pair[1] + '\n' + \
	'The least likely pair of genres to occur are ' + least_likely_genre_pair[0] + ' and ' + least_likely_genre_pair[1])