from fastapi import FastAPI, Query
import json
import requests
import pickle
import pandas as pd

model_for_newuser = open("C:/Users/Pravallika Gajul/Downloads/movielens/newuser.sav","rb")
newuser_model = pickle.load(model_for_newuser)

app = FastAPI()

@app.get('/')   
def login_page():
    print("Message Received")
    return {"message":"LOGIN"}

@app.get('/newuser/')
def read_main():
    print("Message Received new user")
    print(newuser_model)
    return{newuser_model.to_json()}


@app.get('/returninguser/{title}')
def returning_user(title:str):
    print("Message Received returning user")
    print(title)
    output=make_recommendation(model_knn=model_knn,data=movie_user_mat_sparse,fav_movie=title,mapper=movie_to_idx,n_recommendations=10)
    finaloutput=json.dumps(output)
    return{finaloutput}


movies=pd.read_csv("C:/Users/Pravallika Gajul/Downloads/movielens/movies.csv")
ratings=pd.read_csv("C:/Users/Pravallika Gajul/Downloads/movielens/ratings.csv")
df_mid=pd.merge(movies,ratings)
tags=pd.read_csv("C:/Users/Pravallika Gajul/Downloads/movielens/tags.csv")
df_final=pd.merge(df_mid,tags)

from scipy.sparse import csr_matrix
# pivot ratings into movie features
df_ratingbased= ratings.pivot(
    index='movieId',
    columns='userId',
    values='rating'
).fillna(0)
# convert dataframe of movie features to scipy sparse matrix
mat_movie_features = csr_matrix(df_ratingbased.values)

# pivot and create movie-user matrix
movie_user_mat = ratings.pivot(index='movieId', columns='userId', values='rating').fillna(0)
# create mapper from movie title to index
movie_to_idx = {
    movie: i for i, movie in 
    enumerate(list(movies.set_index('movieId').loc[movie_user_mat.index].title))
}
# transform matrix to scipy sparse matrix
movie_user_mat_sparse = csr_matrix(movie_user_mat.values)

# define model
from sklearn.neighbors import NearestNeighbors
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
# fit
model_knn.fit(movie_user_mat_sparse)

from fuzzywuzzy import fuzz
def fuzzy_matching(mapper, fav_movie, verbose=True):
   
    match_tuple = []
    # get match
    for title, idx in mapper.items():
        ratio = fuzz.ratio(title.lower(), fav_movie.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # sort
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        print('Oops! No match is found')
        return
    if verbose:
        print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
    return match_tuple[0][1]

def make_recommendation(model_knn, data, mapper, fav_movie, n_recommendations):

    # fit
    model_knn.fit(data)
    
    # get input movie index
    print('You have input movie:', fav_movie)
    idx = fuzzy_matching(mapper, fav_movie, verbose=True)
    print(idx)
    # inference
    print('Recommendation system start to make inference')
    print('......\n')
    distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations+1)
    print(distances)
    print(indices)
    # get list of raw idx of recommendations
    raw_recommends = \
        sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
    print(raw_recommends)
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    print(reverse_mapper)
    # print recommendations
    print('Recommendations for {}:'.format(fav_movie))
    ans={}
    for i, (idx, dist) in enumerate(raw_recommends):
        ans[i]=('{0}: {1}'.format(i+1, reverse_mapper[idx], dist))
        print(ans)
    return(ans)
