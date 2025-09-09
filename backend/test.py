# # import numpy as np
# # import pandas as pd
# # from sklearn.feature_extraction.text import CountVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity
# # from flask import Flask, request, jsonify
# # from flask_cors import CORS  # Import CORS
# # import ast
# # import nltk
# # from nltk.stem.porter import PorterStemmer

# # # Initialize Flask app
# # app = Flask(__name__)
# # CORS(app)  # Enable CORS for all routes

# # # Load the dataset
# # movies = pd.read_csv('./data/tmdb_5000_movies.csv')
# # credits = pd.read_csv('./data/tmdb_5000_credits.csv')

# # # Merge the datasets
# # movies = movies.merge(credits, on='title')

# # # Select relevant columns
# # movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# # # Drop rows with missing values
# # movies.dropna(inplace=True)

# # # Function to convert stringified lists to actual lists
# # def convert(obj):
# #     L = []
# #     for i in ast.literal_eval(obj):
# #         L.append(i['name'])
# #     return L

# # # Apply the conversion function to genres and keywords
# # movies['genres'] = movies['genres'].apply(convert)
# # movies['keywords'] = movies['keywords'].apply(convert)

# # # Function to fetch the top 3 cast members
# # def convert3(obj):
# #     L = []
# #     counter = 0
# #     for i in ast.literal_eval(obj):
# #         if counter != 3:
# #             L.append(i['name'])
# #             counter += 1
# #         else:
# #             break
# #     return L

# # # Apply the function to cast
# # movies['cast'] = movies['cast'].apply(convert3)

# # # Function to fetch the director from the crew
# # def fetch_director(obj):
# #     L = []
# #     for i in ast.literal_eval(obj):
# #         if i['job'] == 'Director':
# #             L.append(i['name'])
# #             break
# #     return L

# # # Apply the function to crew
# # movies['crew'] = movies['crew'].apply(fetch_director)

# # # Convert overview to list
# # movies['overview'] = movies['overview'].apply(lambda x: x.split())

# # # Remove spaces between words
# # movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
# # movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
# # movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
# # movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# # # Create tags column
# # movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# # # Create a new dataframe with only relevant columns
# # new_df = movies[['movie_id', 'title', 'tags']]

# # # Convert tags to lowercase
# # new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

# # # Initialize PorterStemmer
# # ps = PorterStemmer()

# # # Function to stem words
# # def stem(text):
# #     y = []
# #     for i in text.split():
# #         y.append(ps.stem(i))
# #     return " ".join(y)

# # # Apply stemming to tags
# # new_df['tags'] = new_df['tags'].apply(stem)

# # # Vectorize the tags
# # cv = CountVectorizer(max_features=5000, stop_words='english')
# # vectors = cv.fit_transform(new_df['tags']).toarray()

# # # Calculate cosine similarity
# # similarity = cosine_similarity(vectors)

# # # Function to recommend movies
# # def recommend(movie, count=6):
# #     try:
# #         movie_index = new_df[new_df['title'] == movie].index[0]
# #         distances = similarity[movie_index]
# #         movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:count+1]
# #         recommended_movies = []
# #         for i in movie_list:
# #             recommended_movies.append(new_df.iloc[i[0]].title)
# #         return recommended_movies
# #     except IndexError:
# #         return []
# #     except Exception as e:
# #         print(f"Error in recommend function: {str(e)}")
# #         return []

# # # Get movie details
# # def get_movie_details(title):
# #     try:
# #         movie_data = movies[movies['title'] == title].iloc[0]
# #         return {
# #             'title': movie_data['title'],
# #             'overview': ' '.join(movie_data['overview']),
# #             'genres': movie_data['genres'],
# #             'cast': movie_data['cast'],
# #             'director': movie_data['crew'][0] if movie_data['crew'] else 'Unknown'
# #         }
# #     except IndexError:
# #         return None
# #     except Exception as e:
# #         print(f"Error in get_movie_details function: {str(e)}")
# #         return None

# # # API endpoint to get all movies
# # @app.route('/movies', methods=['GET'])
# # def get_all_movies():
# #     try:
# #         all_movies = new_df['title'].tolist()
# #         return jsonify({'movies': all_movies})
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # # API endpoint to get movie details
# # @app.route('/movie/<title>', methods=['GET'])
# # def movie_details(title):
# #     details = get_movie_details(title)
# #     if details:
# #         return jsonify(details)
# #     else:
# #         return jsonify({'error': 'Movie not found'}), 404

# # # API endpoint to get recommendations
# # @app.route('/recommend', methods=['POST'])
# # def get_recommendations():
# #     try:
# #         data = request.json
# #         title = data.get('title')
# #         count = data.get('count', 6)
        
# #         if not title:
# #             return jsonify({'error': 'No movie title provided'}), 400
        
# #         recommendations = recommend(title, count)
        
# #         if not recommendations:
# #             return jsonify({'error': 'Movie not found or no recommendations available'}), 404
            
# #         return jsonify({'recommended_movies': recommendations})
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # # Run the Flask app
# # if __name__ == '__main__':
# #     app.run(debug=True, host='0.0.0.0', port=5000)

# import pandas as pd
# import requests
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.neighbors import NearestNeighbors
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import nltk
# from nltk.stem.porter import PorterStemmer
# import time
# from functools import lru_cache

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# # Add CORS headers to all responses
# @app.after_request
# def add_cors_headers(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     return response

# # TMDB API configuration
# TMDB_API_KEY = "77033475800632956d4e5a63c2571730"  # Replace with your actual API key
# TMDB_BASE_URL = "https://api.themoviedb.org/3"

# # Create cache for API responses - using string endpoint + params as key
# @lru_cache(maxsize=1000)
# def tmdb_api_request(endpoint, **params):
#     """Make a request to TMDB API with caching to avoid rate limits"""
#     if not params:
#         params = {}
#     params['api_key'] = TMDB_API_KEY
    
#     url = f"{TMDB_BASE_URL}/{endpoint}"
#     response = requests.get(url, params=params)
    
#     # Handle rate limiting
#     if response.status_code == 429:
#         retry_after = int(response.headers.get('Retry-After', 1))
#         time.sleep(retry_after)
#         return tmdb_api_request(endpoint, **params)
    
#     # Handle other errors
#     if response.status_code != 200:
#         print(f"API Error: {response.status_code} - {response.text}")
#         return None
    
#     return response.json()

# # Load initial dataset for initialization and to create our embedding model
# print("Loading initial dataset for model training...")
# movies = pd.read_csv('./data/movies_metadata.csv', low_memory=False)
# credits = pd.read_csv('./data/credits.csv')

# # Clean and merge datasets for initial vectorization
# movies = movies.dropna(subset=['title'])
# movies['id'] = pd.to_numeric(movies['id'], errors='coerce')
# movies = movies.dropna(subset=['id'])
# movies = movies.merge(credits, on='id')

# # Add missing columns if they don't exist
# if 'keywords' not in movies.columns:
#     movies['keywords'] = '[]'

# # Helper functions
# def safe_literal_eval(x):
#     if pd.isna(x):
#         return []
#     try:
#         import ast
#         return ast.literal_eval(x)
#     except:
#         return []

# def get_director(crew):
#     for member in safe_literal_eval(crew):
#         if member.get('job') == 'Director':
#             return member.get('name', '')
#     return ''

# def get_cast(cast):
#     return [actor.get('name', '') for actor in safe_literal_eval(cast)][:3]

# def get_genres(genres):
#     return [genre.get('name', '') for genre in safe_literal_eval(genres)]

# def get_keywords(keywords):
#     if pd.isna(keywords):
#         return []
#     return [kw.get('name', '') for kw in safe_literal_eval(keywords)]

# # Process data columns
# movies['director'] = movies['crew'].apply(get_director)
# movies['cast'] = movies['cast'].apply(get_cast)
# movies['genres'] = movies['genres'].apply(get_genres)
# movies['keywords'] = movies['keywords'].apply(get_keywords)

# # Create tags with proper null handling
# movies['tags'] = (
#     movies['overview'].fillna('') + ' ' +
#     movies['genres'].apply(lambda x: ' '.join(x)) + ' ' +
#     movies['cast'].apply(lambda x: ' '.join(x)) + ' ' +
#     movies['director'].fillna('') + ' ' +
#     movies['keywords'].apply(lambda x: ' '.join(x))
# )

# # Stemming
# ps = PorterStemmer()
# def stem(text):
#     return ' '.join([ps.stem(word) for word in text.split()])

# movies['tags'] = movies['tags'].apply(stem)

# # Vectorization
# cv = CountVectorizer(max_features=3000, stop_words='english')
# vectors = cv.fit_transform(movies['tags'])

# # Nearest Neighbors model
# nn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)
# nn.fit(vectors)

# # Cache movie details from TMDB API - using movie_id (which is an integer) as key
# @lru_cache(maxsize=500)
# def get_movie_details_from_tmdb(movie_id):
#     """Get movie details from TMDB API"""
#     details = tmdb_api_request(f"movie/{movie_id}")
#     if not details:
#         return None
    
#     # Get credits in a separate call
#     credits = tmdb_api_request(f"movie/{movie_id}/credits")
#     if credits:
#         cast = [person.get('name', '') for person in credits.get('cast', [])[:3]]
        
#         director = ''
#         for crew_member in credits.get('crew', []):
#             if crew_member.get('job') == 'Director':
#                 director = crew_member.get('name', '')
#                 break
#     else:
#         cast = []
#         director = ''
    
#     # Get keywords in a separate call
#     keywords_data = tmdb_api_request(f"movie/{movie_id}/keywords")
#     keywords = [kw.get('name', '') for kw in keywords_data.get('keywords', [])] if keywords_data else []
    
#     return {
#         'id': movie_id,
#         'title': details.get('title', ''),
#         'overview': details.get('overview', ''),
#         'genres': [genre.get('name', '') for genre in details.get('genres', [])],
#         'cast': cast,
#         'director': director,
#         'keywords': keywords,
#         'poster_path': details.get('poster_path', ''),
#         'vote_average': details.get('vote_average', 0),
#         'release_date': details.get('release_date', ''),
#         'popularity': details.get('popularity', 0)
#     }

# # Get popular movie titles - no parameters
# @lru_cache(maxsize=1)
# def get_all_movie_titles():
#     """Get all popular movies from TMDB API for dropdown suggestions"""
#     movie_list = []
    
#     # Get multiple pages of popular movies
#     for page in range(1, 6):  # First 5 pages of popular movies
#         popular_movies = tmdb_api_request(f"movie/popular?page={page}")
#         if popular_movies and 'results' in popular_movies:
#             for movie in popular_movies['results']:
#                 movie_list.append({
#                     'id': movie['id'],
#                     'title': movie['title']
#                 })
    
#     # Also get top rated movies
#     for page in range(1, 4):  # First 3 pages of top rated
#         top_movies = tmdb_api_request(f"movie/top_rated?page={page}")
#         if top_movies and 'results' in top_movies:
#             for movie in top_movies['results']:
#                 movie_list.append({
#                     'id': movie['id'],
#                     'title': movie['title']
#                 })
    
#     # Remove duplicates
#     unique_movies = {movie['id']: movie for movie in movie_list}.values()
#     return list(unique_movies)

# def get_poster_url(poster_path, size='w500'):
#     """Generate full URL for a movie poster"""
#     if not poster_path:
#         return ''
#     # Remove leading slash if present
#     clean_path = poster_path.lstrip('/')
#     return f"https://image.tmdb.org/t/p/{size}/{clean_path}"

# # Search movie by title - using the title string as key
# @lru_cache(maxsize=200)
# def search_movie_by_title(title):
#     """Search for a movie by title using TMDB API"""
#     search_results = tmdb_api_request(f"search/movie?query={title}")
#     if not search_results or 'results' not in search_results or not search_results['results']:
#         return None
    
#     # Return the most relevant result
#     return search_results['results'][0]

# # Get recommendations from TMDB - using movie_id (integer) as key
# @lru_cache(maxsize=200)
# def get_recommendations_from_tmdb(movie_id, count=6):
#     """Get movie recommendations from TMDB API"""
#     recommendations = tmdb_api_request(f"movie/{movie_id}/recommendations")
#     if not recommendations or 'results' not in recommendations:
#         return []
    
#     results = recommendations['results'][:count]
    
#     # Fetch genre names for each movie
#     genre_map = {}
#     for movie in results:
#         if 'genre_ids' in movie:
#             movie['genres'] = []
#             for genre_id in movie.get('genre_ids', []):
#                 if genre_id not in genre_map:
#                     # Look up genre name
#                     genre_name = get_genre_name(genre_id)
#                     genre_map[genre_id] = genre_name
#                 movie['genres'].append(genre_map[genre_id])
    
#     return [
#         {
#             'id': movie['id'],
#             'title': movie['title'],
#             'poster_path': movie['poster_path'],
#             'vote_average': movie['vote_average'],
#             'genres': movie.get('genres', [])
#         }
#         for movie in results
#     ]

# # Helper to get genre name from ID
# @lru_cache(maxsize=50)
# def get_genre_name(genre_id):
#     """Get genre name from genre ID"""
#     genres = tmdb_api_request("genre/movie/list")
#     if genres and 'genres' in genres:
#         for genre in genres['genres']:
#             if genre['id'] == genre_id:
#                 return genre['name']
#     return "Unknown"

# def get_similar_movies_from_model(movie_title, count=6):
#     """Get movie recommendations using our local ML model"""
#     try:
#         movie_row = movies[movies['title'] == movie_title]
#         if movie_row.empty:
#             return []
            
#         idx = movie_row.index[0]
#         query_vector = vectors[idx]
#         distances, indices = nn.kneighbors(query_vector, n_neighbors=count+1)
#         movie_indices = indices[0][1:count+1]
        
#         return movies.iloc[movie_indices][['title', 'poster_path', 'vote_average', 'genres']].to_dict('records')
#     except Exception as e:
#         print(f"Model recommendation error: {e}")
#         return []

# # API Endpoints
# @app.route('/movies', methods=['GET'])
# def get_all_movies():
#     try:
#         movie_list = get_all_movie_titles()
#         return jsonify({'movies': [movie['title'] for movie in movie_list]})
#     except Exception as e:
#         print(f"Error fetching movies: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/movie/<title>', methods=['GET'])
# def get_movie(title):
#     try:
#         # First search for the movie
#         search_result = search_movie_by_title(title)
#         if not search_result:
#             return jsonify({'error': 'Movie not found'}), 404
        
#         # Then get detailed information
#         movie_id = search_result['id']
#         movie = get_movie_details_from_tmdb(movie_id)
        
#         if not movie:
#             return jsonify({'error': 'Failed to get movie details'}), 404
            
#         return jsonify({
#             'id': movie['id'],
#             'title': movie['title'],
#             'overview': movie['overview'],
#             'genres': movie['genres'],
#             'cast': movie['cast'],
#             'director': movie['director'],
#             'poster': get_poster_url(movie['poster_path']),
#             'rating': float(movie['vote_average']),
#             'release_date': movie['release_date']
#         })
#     except Exception as e:
#         print(f"Error fetching movie: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/recommend', methods=['POST'])
# def get_recommendations():
#     try:
#         data = request.json
#         title = data.get('title')
#         count = int(data.get('count', 6))
        
#         if not title:
#             return jsonify({'error': 'No title provided'}), 400
        
#         # Search for movie by title
#         search_result = search_movie_by_title(title)
#         if not search_result:
#             # Fallback to model-based recommendations if TMDB search fails
#             model_recommendations = get_similar_movies_from_model(title, count)
#             if not model_recommendations:
#                 return jsonify({'error': 'Movie not found'}), 404
                
#             return jsonify({
#                 'recommended_movies': [
#                     {
#                         'title': movie['title'],
#                         'poster': get_poster_url(movie.get('poster_path')),
#                         'rating': float(movie['vote_average']) if pd.notnull(movie['vote_average']) else 0.0,
#                         'genres': movie['genres']
#                     } 
#                     for movie in model_recommendations
#                 ],
#                 'source': 'model'
#             })
        
#         # Get recommendations from TMDB API
#         movie_id = search_result['id']
#         api_recommendations = get_recommendations_from_tmdb(movie_id, count)
        
#         # If API recommendations are empty, fall back to model
#         if not api_recommendations:
#             model_recommendations = get_similar_movies_from_model(title, count)
#             if not model_recommendations:
#                 return jsonify({'error': 'No recommendations found'}), 404
                
#             return jsonify({
#                 'recommended_movies': [
#                     {
#                         'title': movie['title'],
#                         'poster': get_poster_url(movie.get('poster_path')),
#                         'rating': float(movie['vote_average']) if pd.notnull(movie['vote_average']) else 0.0,
#                         'genres': movie['genres']
#                     } 
#                     for movie in model_recommendations
#                 ],
#                 'source': 'model'
#             })
        
#         # Return API recommendations
#         return jsonify({
#             'recommended_movies': [
#                 {
#                     'title': movie['title'],
#                     'poster': get_poster_url(movie['poster_path']),
#                     'rating': float(movie['vote_average']),
#                     'genres': movie['genres']
#                 } 
#                 for movie in api_recommendations
#             ],
#             'source': 'tmdb'
#         })
#     except Exception as e:
#         print(f"Recommendation API error: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/search', methods=['GET'])
# def search_movies():
#     query = request.args.get('query', '')
#     if not query:
#         return jsonify({'results': []}), 400
        
#     search_results = tmdb_api_request(f"search/movie?query={query}")
#     if not search_results or 'results' not in search_results:
#         return jsonify({'results': []}), 404
        
#     return jsonify({
#         'results': [
#             {
#                 'id': movie['id'],
#                 'title': movie['title'],
#                 'poster': get_poster_url(movie.get('poster_path')),
#                 'year': movie.get('release_date', '')[:4] if movie.get('release_date') else ''
#             }
#             for movie in search_results['results'][:10]  # Limit to top 10 results
#         ]
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)