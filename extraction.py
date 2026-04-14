import pandas as pd
import pickle
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies=pd.read_csv("tmdb_5000_movies.csv")
credits=pd.read_csv("tmdb_5000_credits.csv")

merged=movies.merge(credits,on="title")

merged=merged[['movie_id','title','genres','overview','keywords','vote_average','cast','crew']]

merged['overview']=merged['overview'].fillna('')

def convert(text):
    l=[]
    for i in ast.literal_eval(text):
        l.append(i['name'])
    return l

def top3_cast(text):
    c=[]
    count=0
    for i in ast.literal_eval(text):
        if count<3:
            c.append(i['name'])
            count+=1
        else:
            break
    return c

def director(text):
    d=[]
    for i in ast.literal_eval(text):
        if(i['job']=='Director'):
            d.append(i['name'])
    return d

def extract(text):
    try:
        return text.split()
    except:
        return []

merged['genres']=merged['genres'].apply(convert)
merged['keywords']=merged['keywords'].apply(convert)
merged['cast']=merged['cast'].apply(top3_cast)
merged['crew']=merged['crew'].apply(director)
merged['overview']=merged['overview'].apply(extract)

def spaces(text):
    result=[]
    for i in text:
        result.append(i.replace(" ",""))
    return result

merged['genres']=merged['genres'].apply(spaces)
merged['keywords']=merged['keywords'].apply(spaces)
merged['cast']=merged['cast'].apply(spaces)
merged['crew']=merged['crew'].apply(spaces)

merged['tags']=merged['genres'] + merged['overview']+merged['keywords']+merged['cast']+merged['crew']

new_df=merged[['movie_id','title','vote_average','tags']].copy()

def list_to_text(text):
    return " ".join(text)

new_df['tags']=new_df['tags'].apply(list_to_text)
new_df['tags'] = new_df['tags'].apply(str.lower)

cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()

similar=cosine_similarity(vectors)

pickle.dump(new_df,open("movies.pkl","wb"))
pickle.dump(similar,open("similar.pkl",'wb'))