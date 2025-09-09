from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time
import json
import os
import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import hashlib

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configuration
TMDB_API_KEY = "acbafe412afa10d645c49fe59fd663c4"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
CACHE_DIR = "api_cache"
ML_CACHE_DIR = "ml_model_cache"
DATA_REFRESH_HOURS = 24

# Initialize components
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))
executor = ThreadPoolExecutor(max_workers=4)

# Global variables for ML model
movie_data = pd.DataFrame()
tfidf_matrix = None
cosine_sim = None
last_refresh_time = 0

# Sample fallback data
SAMPLE_MOVIES = ["The Dark Knight", "Inception", "Interstellar", "The Matrix", "Pulp Fiction"]
SAMPLE_MOVIE_DETAILS = {
    "The Dark Knight": {
        "title": "The Dark Knight",
        "overview": "Batman raises the stakes in his war on crime...",
        "genres": ["Action", "Drama"],
        "cast": ["Christian Bale", "Heath Ledger"],
        "director": "Christopher Nolan",
        "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "rating": 8.5
    }
}

def initialize_model():
    global movie_data, tfidf_matrix, cosine_sim, last_refresh_time
    try:
        if os.path.exists(os.path.join(ML_CACHE_DIR, 'movie_data.pkl')):
            movie_data = pd.read_pickle(os.path.join(ML_CACHE_DIR, 'movie_data.pkl'))
            tfidf_matrix = np.load(os.path.join(ML_CACHE_DIR, 'tfidf_matrix.npy'))
            cosine_sim = np.load(os.path.join(ML_CACHE_DIR, 'cosine_sim.npy'))
            last_refresh_time = os.path.getmtime(os.path.join(ML_CACHE_DIR, 'movie_data.pkl'))
            print("Loaded cached ML model")
            return
    except Exception as e:
        print(f"Error loading model: {str(e)}")
    refresh_movie_data()

def fetch_tmdb_dataset(pages=5):
    movies = []
    for page in range(1, pages+1):
        data = tmdb_api_request("movie/popular", page=page)
        time.sleep(0.5)  
        if data and 'results' in data:
            movies.extend(data['results'])
    
    # Check if we got any movies
    if not movies:
        # Return an empty DataFrame with the required columns
        return pd.DataFrame(columns=['id', 'title', 'overview', 'genre_ids'])
    
    # Make sure all required columns exist
    df = pd.DataFrame(movies)
    for col in ['id', 'title', 'overview', 'genre_ids']:
        if col not in df.columns:
            df[col] = None if col != 'genre_ids' else df.apply(lambda x: [], axis=1)
            
    return df[['id', 'title', 'overview', 'genre_ids']]

def preprocess_data(df):
    df['genres'] = df['genre_ids'].apply(lambda x: get_genre_names(tuple(x)))
    df['director'] = df['id'].apply(get_director)
    df['cast'] = df['id'].apply(get_cast)
    df['overview'] = df['overview'].fillna('')
    
    df['combined_features'] = df.apply(lambda x: 
        f"{x['overview']} {' '.join(x['genres'])} {x['director']} {' '.join(x['cast'])}", axis=1)
    df['combined_features'] = df['combined_features'].apply(
        lambda x: ' '.join([ps.stem(word) for word in x.split() if word.lower() not in stop_words]))
    
    return df

def refresh_movie_data():
    global movie_data, tfidf_matrix, cosine_sim, last_refresh_time
    print("Refreshing ML model data...")
    movies = fetch_tmdb_dataset(pages=5)
    
    if movies.empty:
        print("Failed to fetch movie data, using default empty model")
        movie_data = pd.DataFrame(columns=['id', 'title', 'combined_features'])
        tfidf_matrix = np.array([])
        cosine_sim = np.array([])
        return
    
    movies = preprocess_data(movies)
    tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    
    if movies.empty or movies['combined_features'].isnull().all():
        print("No valid features to process")
        movie_data = movies
        tfidf_matrix = np.array([])
        cosine_sim = np.array([])
        return
        
    tfidf_matrix = tfidf.fit_transform(movies['combined_features'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    os.makedirs(ML_CACHE_DIR, exist_ok=True)
    movies.to_pickle(os.path.join(ML_CACHE_DIR, 'movie_data.pkl'))
    np.save(os.path.join(ML_CACHE_DIR, 'tfidf_matrix.npy'), tfidf_matrix)
    np.save(os.path.join(ML_CACHE_DIR, 'cosine_sim.npy'), cosine_sim)
    last_refresh_time = time.time()
    movie_data = movies
    print("ML model updated")

@lru_cache(maxsize=1000)
def tmdb_api_request(endpoint, **params):
    params['api_key'] = TMDB_API_KEY
    
    # Generate a safe filename using hash to avoid path issues
    param_str = '_'.join(f'{k}={v}' for k, v in sorted(params.items()))
    cache_key = hashlib.md5(f"{endpoint}_{param_str}".encode()).hexdigest()
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    # Check if cache exists and is valid
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Cache read error: {str(e)}")
    
    # Make the API request
    try:
        url = f"{TMDB_BASE_URL}/{endpoint}"
        print(f"Requesting: {url} with params {params}")
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Save to cache
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(cache_file, 'w') as f:
                json.dump(data, f)
            
            return data
        else:
            print(f"API error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"API Error: {str(e)}")
    
    return None

def get_poster_url(poster_path):
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

@lru_cache(maxsize=1000)
def get_genre_names(genre_ids):
    genres_data = tmdb_api_request("genre/movie/list") or {}
    if not genre_ids:
        return []
    return [g['name'] for g in genres_data.get('genres', []) if g['id'] in genre_ids]

@lru_cache(maxsize=1000)
def get_director(movie_id):
    credits = tmdb_api_request(f"movie/{movie_id}/credits") or {}
    for crew in credits.get('crew', []):
        if crew.get('job') == 'Director':
            return crew.get('name', '')
    return ''

@lru_cache(maxsize=1000)
def get_cast(movie_id):
    credits = tmdb_api_request(f"movie/{movie_id}/credits") or {}
    return [cast.get('name', '') for cast in credits.get('cast', [])[:3]]

def get_ml_recommendations(title, count=5):
    try:
        if movie_data.empty or tfidf_matrix.size == 0 or cosine_sim.size == 0:
            return []
            
        indices = pd.Series(movie_data.index, index=movie_data['title']).drop_duplicates()
        if title not in indices:
            return []
            
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:count+1]
        return movie_data.iloc[[i[0] for i in sim_scores]][['id', 'title']].to_dict('records')
    except Exception as e:
        print(f"ML recommendation error: {str(e)}")
        return []

def get_tmdb_recommendations(title, count=5):
    search = tmdb_api_request("search/movie", query=title)
    if not search or not search.get('results'):
        return []
    
    movie_id = search['results'][0]['id']
    recs = tmdb_api_request(f"movie/{movie_id}/recommendations")
    if not recs or not recs.get('results'):
        return []
    
    return [{
        'id': m['id'],
        'title': m['title'],
        'poster': get_poster_url(m.get('poster_path')),
        'rating': m.get('vote_average', 0),
    } for m in recs['results'][:count]]

@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        data = tmdb_api_request("movie/popular") or {}
        return jsonify([m['title'] for m in data.get('results', [])[:50]])
    except Exception as e:
        print(f"Error getting movies: {str(e)}")
        return jsonify(SAMPLE_MOVIES)

@app.route('/movie/<title>', methods=['GET'])
def get_movie(title):
    try:
        search = tmdb_api_request("search/movie", query=title)
        if not search or not search.get('results'):
            return jsonify(SAMPLE_MOVIE_DETAILS.get(title, {}))
        
        movie_id = search['results'][0]['id']
        details = tmdb_api_request(f"movie/{movie_id}")
        credits = tmdb_api_request(f"movie/{movie_id}/credits")
        
        return jsonify({
            'title': details.get('title', ''),
            'overview': details.get('overview', ''),
            'genres': [g['name'] for g in details.get('genres', [])],
            'cast': [c['name'] for c in credits.get('cast', [])[:3]],
            'director': get_director(movie_id),
            'poster': get_poster_url(details.get('poster_path')),
            'rating': details.get('vote_average', 0)
        })
    except Exception as e:
        print(f"Error getting movie details: {str(e)}")
        return jsonify(SAMPLE_MOVIE_DETAILS.get(title, {}))

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    title = data.get('title')
    count = int(data.get('count', 6))
    
    if time.time() - last_refresh_time > DATA_REFRESH_HOURS * 3600:
        executor.submit(refresh_movie_data)
    
    ml_recs = [enrich_ml_recommendation(m) for m in get_ml_recommendations(title, count//2)]
    tmdb_recs = get_tmdb_recommendations(title, count//2)
    
    combined = []
    seen = set()
    for rec in ml_recs + tmdb_recs:
        if rec['title'] not in seen:
            combined.append(rec)
            seen.add(rec['title'])
    
    return jsonify({'results': combined[:count]})

def enrich_ml_recommendation(movie):
    details = tmdb_api_request(f"movie/{movie['id']}") or {}
    return {
        'title': movie['title'],
        'poster': get_poster_url(details.get('poster_path')),
        'rating': details.get('vote_average', 0),
        'genres': [g['name'] for g in details.get('genres', [])]
    }

if __name__ == '__main__':
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(ML_CACHE_DIR, exist_ok=True)
    initialize_model()
    app.run(debug=True, port=5000)