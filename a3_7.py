#Question 7, application_1524406905265_3277 on full dataset
from pyspark import SparkContext, SparkConf
from math import sqrt
sc = SparkContext.getOrCreate()
movie_id = 3
def parse_with_commas(x):
	if x.count(',')>2:
		return [x[:x.find(',')], x[x.find(',')+2:x.rfind(',')-1], x[x.rfind(',')+1:]]
	else:
		return x.split(',')

def calculate_euclidean_dist(x):
	y = x[1]
	movie_1 = y[0][1]
	movie_2 = y[1][1]
	sum = 0
	min = 1150
	max = 0
	for i in range(len(movie_1)):
		movie_1[i][0] = int(movie_1[i][0])
		if movie_1[i][0] > max:
			max = movie_1[i][0]
		if movie_1[i][0] <= min:
			min = movie_1[i][0]
		movie_1[i][1] = float(movie_1[i][1])
	for i in range(len(movie_2)):
		movie_2[i][0] = int(movie_2[i][0])
		if movie_2[i][0] > max:
			max = movie_2[i][0]
		if movie_2[i][0] <= min:
			min = movie_2[i][0]
		movie_2[i][1] = float(movie_2[i][1])
		
	for i in range(min, max + 1):
		score_1 = 0
		score_2 = 0
		for j in range(len(movie_1)):
			if i==movie_1[j][0]:
				score_1 = movie_1[j][1]
				break
		for j in range(len(movie_2)):
			if i==movie_2[j][0]:
				score_2 = movie_2[j][1]
				
		sum = sum + (score_1 - score_2)**2
	
	return (y[1][0], sqrt(sum))
	
movies = sc.textFile("hdfs:///user/simmhan/ml/full/movies.csv").cache()
genome = sc.textFile("hdfs:///user/simmhan/ml/full/genome-scores.csv").cache()
rdd_genome = genome.map(lambda x:x.split(',')).filter(lambda z:z[0] != 'movieId').map(lambda y:(y[0],[y[1],y[2]]))
rdd_genome_grouped = rdd_genome.groupByKey().mapValues(list)
rdd_movie_compared = rdd_genome_grouped.filter(lambda x:x[0] == str(movie_id)).map(lambda y:(1, y))
rdd_all_movies = rdd_genome_grouped.map(lambda x:(1, x))
rdd_side_by_side = rdd_movie_compared.join(rdd_all_movies)
rdd_distance = rdd_side_by_side.map(calculate_euclidean_dist)
rdd_movies = movies.map(parse_with_commas).filter(lambda z:z[0] != 'movieId').map(lambda x:(x[0], x[1]))
rdd_joined = rdd_movies.join(rdd_distance)
rdd_sorted = rdd_joined.sortBy(lambda x:x[1][1]).map(lambda y:y[1][0])
rdd_top_10 = rdd_sorted.take(11)
print('The top 10 movies which has nearest euclidean distance are\n')
for movie in rdd_top_10[1:]:
	print(movie + '\n')