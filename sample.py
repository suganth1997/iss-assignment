from pyspark import SparkContext, SparkConf
 
sc = SparkContext.getOrCreate()

#sc.textFile("hdfs:///user/simmhan/ml/small/ratings.csv").take(10)

#Question 1

ratings = sc.textFile("hdfs:///user/simmhan/ml/small/ratings.csv").cache()
raters_distinct_user_ids = ratings.map(lambda x:x.split(',')).map(lambda y:y[0]).distinct()
distinct_users_rated = raters_distinct_user_ids.count()

tagged = sc.textFile("hdfs:///user/simmhan/ml/small/tags.csv").cache()
tagers_distinct_user_id = tagged.map(lambda x:x.split(',')).map(lambda y:y[0]).distinct()
distinct_users_tagged = tagers_distinct_user_id.count()

users_both_rated_and_tagged = raters_distinct_user_ids.intersection(tagers_distinct_user_id).count()


#Question 2

ratings = sc.textFile("hdfs:///user/simmhan/ml/small/ratings.csv").cache()
avg_num_of_ratings = ratings.map(lambda x:x.split(',')).map(lambda y:(int(y[0]), 1)).groupByKey().mapValues(sum).map(lambda z:z[1]).mean()
avg_val_of_ratings = ratings.map(lambda x:x.split(',')).map(lambda y:int(y[2])).mean()

#Question 3

ratings = sc.textFile("hdfs:///user/simmhan/ml/small/ratings.csv").cache()
rdd_ratings = ratings.map(lambda x:x.split(',')).map(lambda y:int(y[2])).sortBy(lambda z:z).zipWithIndex().map(lambda x:(x[1], x[0]))
median_rating = rdd_ratings.lookup(rdd_ratings.count()/2)

#Question 4

def parse_with_commas(x):
	if x.count(',')>2:
		return [x[:x.find(',')], x[x.find(',')+1:x.rfind(',')], x[x.rfind(',')+1:]]
	else:
		return x.split(',')

movies = sc.textFile("hdfs:///user/simmhan/ml/small/movies.csv").cache()
rdd_movies = movies.map(parse_with_commas).map(lambda x:len(x[2].split('|')))
max_num_genres = rdd_movies.max(key=int)

#Question 5

def parse_with_commas(x):
	if x.count(',')>2:
		return [x[:x.find(',')], x[x.find(',')+1:x.rfind(',')], x[x.rfind(',')+1:]]
	else:
		return x.split(',')

movies = sc.textFile("hdfs:///user/simmhan/ml/small/movies.csv").cache()
rdd_movies = movies.map(parse_with_commas).flatMap(lambda x:x[2].split('|'))
rdd_genres_kv_pair = movies.map(lambda x:(x,1)).groupByKey().mapValues(sum)
max_genre = rdd_genres_kv_pair.max(key = lambda x:x[1])[0]
min_genre = rdd_genres_kv_pair.min(key = lambda x:x[1])[0]

#Question 6

from itertools import combinations
def parse_with_commas(x):
	if x.count(',')>2:
		return [x[:x.find(',')], x[x.find(',')+1:x.rfind(',')], x[x.rfind(',')+1:]]
	else:
		return x.split(',')

movies = sc.textFile("hdfs:///user/simmhan/ml/small/movies.csv").cache()
rdd_genre_pairs = movies.map(parse_with_commas).filter(lambda y: y[2].find('|')!=-1).flatMap(lambda x:list(combinations(x,2)))
genre_kv_pair = rdd_genre_pairs.map(lambda x:(x,1).groupByKey().mapValues(sum)
most_likely_genre_pair = genre_kv_pair.max(key = lambda x:x[1])[0]
least_likely_genre_pair = genre_kv_pair.min(key = lambda x:x[1])[0]

#Question 7

