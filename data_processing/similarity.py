from math import sqrt


def products(pair: tuple):
    """Takes in a (TITLE, ((USER, SCORE1) (USER, SCORE2))) pair and returns
    (TITLE, (SCORE1 * SCORE2, SCORE1 * SCORE1, SCORE2 * SCORE2))))

        ('100 Days with Mr. Arrogant',
        (('https://mydramalist.com/dramalist/Zombie_Girl', 50),
        ('https://mydramalist.com/dramalist/Shifterz', 30)))

    The result will be summed and used to compute cosine similarity
    """
    (user1, score1), (user2, score2) = pair[1]

    if user1 > user2:
        user1, user2 = user2, user1

    return (user1, user2), (score1 * score2, score1 * score1, score2 * score2)


def partial_cosine(df: pyspark.sql.DataFrame):
    score_avgs = df.groupBy('title').avg('score')
    # Finds users who have watched the most shows
    top1000_users = (df
                     .filter('score > 0')
                     .groupBy('user')
                     .count()
                     .sort('count')
                     .limit(1000))
    return top1000_users


# Todo: Refactor the lambdas into named functions
def cosine_similarity(df: pyspark.sql.DataFrame) -> pyspark.rdd:
    """Takes in a Dataframe and uses Spark RDDs to compute
    the cosine similarity.
    """
    rdd = df.rdd

    # Computes the average score of each move
    avgs = (rdd
            .filter(lambda row: row['score'] and row['score'] > 0)
            .map(lambda row: (row['title'], row['score']))
            .combineByKey(lambda score: (score, 1),
                          lambda pair, score: (
                              pair[0] + score, pair[1] + 1),
                          lambda pair1, pair2: (
                              pair1[0] + pair2[0], pair1[1] + pair2[1]))
            .map(lambda tup: (tup[0], tup[1][0] / tup[1][1])))

    # TODO: Include average score col. This is incorrect
    ratings = (rdd
               .filter(lambda row: row['score'] and row['score'] > 0)
               .map(lambda row: (row['title'], (row['user'], row['score']))))


    similarities = (ratings
                    .join(ratings)  # Todo: Check join partitioning
                    # Tuples should contain scores from different users
                    .filter(lambda tup: tup[1][0] != tup[1][1])
                    .map(products)  # Todo: Filter if not enough common shows
                    .reduceByKey(lambda tup1, tup2: (tup1[0] + tup2[0],
                                                     tup1[1] + tup2[1],
                                                     tup1[2] + tup2[2]))
                    .map(lambda tup:
                         (tup[0], tup[1][0] / sqrt(tup[1][1] * tup[1][2])))
                    .map(lambda tup:
                         '{},{},{}'.format(tup[0][0], tup[0][1], tup[1])))

    return similarities