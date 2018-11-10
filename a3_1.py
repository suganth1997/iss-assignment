#application_1524406905265_3219 on small dataset
#application_1524406905265_3283 on full dataset
#Question 1(a) 
from pyspark import SparkContext, SparkConf
 
sc = SparkContext.getOrCreate()
ratings = sc.textFile("hdfs:///user/simmhan/ml/small/ratings.csv").cache()
raters_distinct_user_ids = ratings.map(lambda x:x.split(',')).filter(lambda z:z[0] != 'userId').map(lambda y:y[0]).distinct()
distinct_users_rated = raters_distinct_user_ids.count()
#print('Distinct Users Rated = ' + str(distinct_users_rated))

#Question 1(b)
tagged = sc.textFile("hdfs:///user/simmhan/ml/small/tags.csv").cache()
tagers_distinct_user_id = tagged.map(lambda x:x.split(',')).filter(lambda z:z[0] != 'userId').map(lambda y:y[0]).distinct()
distinct_users_tagged = tagers_distinct_user_id.count()
#print('Distinct Users Tagged = ' + str(distinct_users_tagged))

#Question 1(c)
users_both_rated_and_tagged = raters_distinct_user_ids.intersection(tagers_distinct_user_id).count()
print('Distinct Users Rated = ' + str(distinct_users_rated) + '\n' + 'Distinct Users Tagged = ' + str(distinct_users_tagged) + '\n' + 'Distinct Users both Rated and Tagged = ' + str(users_both_rated_and_tagged))