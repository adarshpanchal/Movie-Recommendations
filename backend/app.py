from flask import Flask,request,jsonify
from recommendations import recommend
from recommendations import movies
from flask_cors import CORS
app=Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Movie Recommendations API Running"

@app.route('/recommend',methods=['GET'])
def recommend_api():
    movie=request.args.get('movie')

    if not movie:
        return jsonify({'error':"Movie Name is Required"}),400
    
    results=recommend(movie)

    if not results:
        return jsonify({'error':'Movie not found'}) , 404
    return jsonify(results)

@app.route('/search',methods=['GET'])
def search():
    query=request.args.get('query')

    if not query:
        return jsonify([])
    
    query=query.lower()
    matches=movies[movies['title_lower'].str.contains(query)]

    return jsonify(matches['title'].tolist()[:10])
    


if __name__=='__main__':
    app.run(debug=True)