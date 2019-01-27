import math


def average_features(track_features):
    averages = {}
    for features in track_features:
        averages['mode'] += features['mode']
        averages['acousticness'] += features['acousticness']
        averages['danceability'] += features['danceability']
        averages['energy'] += features['energy']
        averages['instrumentalness'] += features['instrumentalness']
        averages['liveness'] += features['liveness']
        averages['loudness'] += features['loudness']
        averages['valence'] += features['valence']
        averages['tempo'] += features['tempo']

    for feature in averages:
        averages[feature] = averages[feature]/len(track_features)

    return averages


def similarity(features1, features2):
    dif_squared = 0
    for feature in features1:
        (features1[feature] - features2[feature]) ** 2
    distance = math.sqrt(dif_squared)
    similarity_score = 1/(1+distance)
    return similarity_score
