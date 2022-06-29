from fileinput import filename
import pandas as pd
import pickle

movies=pd.read_csv("movies.csv")
ratings=pd.read_csv("ratings.csv")
df_final=movies.merge(ratings)


popularmovies=df_final[['title','rating']]
top=popularmovies['title'].value_counts().sort_values(ascending=False)
top10=top.head(10)
print(top10)


filename='newuser.sav'
pickle.dump(top10,open('newuser.sav','wb'))

