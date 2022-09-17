import pandas as pd

from sklearn import ensemble
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from scipy.stats import pearsonr

import csv
import sys


def load_moive_data(path_train, path_validation):
    df_training = pd.read_csv(path_train)
    df_validation = pd.read_csv(path_validation)

    language_set = set(df_training['original_language']).union(df_validation['original_language'])
    language_dict = dict(zip(language_set, range(len(language_set))))

    df_training['cast'] = df_training['cast'].apply(lambda x: x.count("cast_id"))
    df_training['crew'] = df_training['crew'].apply(lambda x: x.count("credit_id"))
    df_training['genres'] = df_training['genres'].apply(lambda x: x.count("name"))
    df_training['keywords'] = df_training['keywords'].apply(lambda x: x.count("name"))
    df_training['original_language'] = df_training['original_language'].apply(lambda x: language_dict[x])
    df_training['production_companies'] = df_training['production_companies'].apply(lambda x: x.count("name"))
    df_training['production_countries'] = df_training['production_countries'].apply(lambda x: x.count("name"))
    df_training['release_date'] = pd.to_datetime(df_training['release_date'])
    df_training['release_date_year'] = df_training['release_date'].dt.year
    df_training['release_date_month'] = df_training['release_date'].dt.month
    df_training['release_date_day'] = df_training['release_date'].dt.day

    df_validation['cast'] = df_validation['cast'].apply(lambda x: x.count("cast_id"))
    df_validation['crew'] = df_validation['crew'].apply(lambda x: x.count("credit_id"))
    df_validation['genres'] = df_validation['genres'].apply(lambda x: x.count("name"))
    df_validation['keywords'] = df_validation['keywords'].apply(lambda x: x.count("name"))
    df_validation['original_language'] = df_validation['original_language'].apply(lambda x: language_dict[x])
    df_validation['production_companies'] = df_validation['production_companies'].apply(lambda x: x.count("name"))
    df_validation['production_countries'] = df_validation['production_countries'].apply(lambda x: x.count("name"))
    df_validation['release_date'] = pd.to_datetime(df_validation['release_date'])
    df_validation['release_date_year'] = df_validation['release_date'].dt.year
    df_validation['release_date_month'] = df_validation['release_date'].dt.month
    df_validation['release_date_day'] = df_validation['release_date'].dt.day

    return df_training, df_validation


def regression_data(df_training, df_validation):
    del df_training['movie_id']
    del df_training['homepage']
    del df_training['original_title']
    del df_training['overview']
    del df_training['spoken_languages']
    del df_training['status']
    del df_training['tagline']
    del df_training['rating']
    del df_training['release_date']
    del df_training['original_language']
    del df_training['genres']
    del df_training['production_countries']

    del df_validation['movie_id']
    del df_validation['homepage']
    del df_validation['original_title']
    del df_validation['overview']
    del df_validation['spoken_languages']
    del df_validation['status']
    del df_validation['tagline']
    del df_validation['rating']
    del df_validation['release_date']
    del df_validation['original_language']
    del df_validation['genres']
    del df_validation['production_countries']

    X_train = df_training.drop('revenue', axis=1).values
    y_train = df_training['revenue'].values

    X_test = df_validation.drop('revenue', axis=1).values
    y_test = df_validation['revenue'].values

    return X_train, y_train, X_test, y_test


def classification_data(df_training, df_validation):
    del df_training['movie_id']
    del df_training['homepage']
    del df_training['original_title']
    del df_training['overview']
    del df_training['spoken_languages']
    del df_training['status']
    del df_training['tagline']
    del df_training['revenue']
    del df_training['release_date']
    del df_training['original_language']
    del df_training['genres']
    del df_training['production_countries']

    del df_validation['movie_id']
    del df_validation['homepage']
    del df_validation['original_title']
    del df_validation['overview']
    del df_validation['spoken_languages']
    del df_validation['status']
    del df_validation['tagline']
    del df_validation['revenue']
    del df_validation['release_date']
    del df_validation['original_language']
    del df_validation['genres']
    del df_validation['production_countries']

    X_train = df_training.drop('rating', axis=1).values
    y_train = df_training['rating'].values

    X_test = df_validation.drop('rating', axis=1).values
    y_test = df_validation['rating'].values

    return X_train, y_train, X_test, y_test


if __name__ == "__main__":
    df_training, df_validation = load_moive_data(sys.argv[1], sys.argv[2])
    movie_id = df_validation['movie_id'].values
    X_train, y_train, X_test, y_test = regression_data(df_training, df_validation)
    model = ensemble.GradientBoostingRegressor()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    file = open('z5248104.PART1.summary.csv', 'w')
    file_write = csv.writer(file)
    file_write.writerow(['zid', 'MSE', 'correlation'])
    p, _ = pearsonr(y_test, y_pred)
    file_write.writerow(['z5248104', round(metrics.mean_squared_error(y_test, y_pred), 2), round(p, 2)])
    file.close()

    file = open('z5248104.PART1.output.csv', 'w')
    file_write = csv.writer(file)
    file_write.writerow(['movie_id', 'predicted_revenue'])
    for i in range(len(y_test)):
        file_write.writerow([movie_id[i], round(y_pred[i],2)])
    file.close()

    df_training, df_validation = load_moive_data("training.csv", "validation.csv")
    X_train, y_train, X_test, y_test = classification_data(df_training, df_validation)

    clf1 = LogisticRegression()
    clf2 = ensemble.RandomForestClassifier()
    clf3 = GaussianNB()
    model = ensemble.VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='soft',
                                      weights=[1, 3, 1],
                                      flatten_transform=True)
    model = model.fit(X_train, y_train)

    # predict the test set
    y_pred = model.predict(X_test)

    file = open('z5248104.PART2.summary.csv', 'w')
    file_write = csv.writer(file)
    file_write.writerow(['zid', 'average_precision', 'average_recall', 'accuracy'])
    file_write.writerow(['z5248104', round(metrics.precision_score(y_test, y_pred, average='macro'), 2),
                         round(metrics.recall_score(y_test, y_pred, average='macro'), 2),
                         round(metrics.accuracy_score(y_test, y_pred), 2)])
    file.close()

    file = open('z5248104.PART2.output.csv', 'w')
    file_write = csv.writer(file)
    file_write.writerow(['movie_id', 'predicted_rating'])
    for i in range(len(y_test)):
        file_write.writerow([movie_id[i], y_pred[i]])
    file.close()
