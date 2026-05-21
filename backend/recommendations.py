import pickle
import requests
from dotenv import load_dotenv
import os
import time
load_dotenv()

movies=pickle.load(open("movies.pkl",'rb'))
similar=pickle.load(open("similar.pkl",'rb'))

movies['title_lower']=movies['title'].str.lower()

def fetch_poster(movie_id):
    api_key=os.getenv("TMDB_API_KEY")
    url= f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    try:
        response=requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()
        data=response.json()

        poster_path=data.get('poster_path')

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
        
    except requests.exceptions.RequestException as e:
        print("Error : ",e)
        return "https://via.placeholder.com/500x750?text=Error"
    
def recommend(movie):
    movie=movie.lower()

    if movie not in movies['title_lower'].values:
        return []
    
    movie_index=movies[movies['title_lower']==movie].index[0]
    distances=similar[movie_index]

    target_director=movies.iloc[movie_index]['director']

    scored_movies=[]

    for i in range(len(distances)):
        similarity_scores=distances[i]
        rating_score=movies.iloc[i].vote_average

        director_bonus=0
        if movies.iloc[i]['director']==target_director:
            director_bonus=0.05
        
        final_score=(0.6*similarity_scores)+(0.35*rating_score)+director_bonus
        scored_movies.append((i,final_score))

    movies_list=sorted(
        scored_movies,
        reverse=True,
        key=lambda x:x[1]
    )[1:11]

    results=[]

    for i in movies_list:
        movie_data=movies.iloc[i[0]]
        results.append({
            'title':str(movie_data.title),
            'movie_id':int(movie_data.movie_id),
            'rating':float(round(movie_data.vote_average*10,1)),
            'poster':fetch_poster(int(movie_data.movie_id))
            })
        time.sleep(0.2)
    return results
    
# print(recommend('Fight Club'))