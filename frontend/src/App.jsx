import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Favorites from './components/Favorites';
import MovieDetails from './components/MovieDetails';
import MovieList from './components/MovieList';
import Footer from './components/Footer';
import LoadingState from './components/LoadingState';
import ErrorState from './components/ErrorState';

// Import GSAP for animations
import { gsap } from 'gsap';

const App = () => {
  // State variables
  const [searchTerm, setSearchTerm] = useState('');
  const [movieSuggestions, setMovieSuggestions] = useState([]);
  const [allMovies, setAllMovies] = useState([]);
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [activeTab, setActiveTab] = useState('search');
  const [darkMode, setDarkMode] = useState(true);
  const [favorites, setFavorites] = useState([]);
  
  // Refs for animations
  const headerRef = useRef(null);
  const heroRef = useRef(null);
  const resultsRef = useRef(null);
  const suggestionBoxRef = useRef(null);
  
  // API base URL
  const API_BASE_URL = 'http://localhost:5000';

  // Fetch all movies for suggestions when component mounts
  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/movies`);
        const data = await response.json();
        
        if (data.movies) {
          setAllMovies(data.movies);
        }
      } catch (error) {
        console.error('Error fetching movies:', error);
      }
    };

    fetchMovies();
    
    // Initial animations
    const tl = gsap.timeline();
    tl.from(headerRef.current, { y: -50, opacity: 0, duration: 0.8, ease: "power3.out" })
      .from(heroRef.current, { y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }, "-=0.4");
  }, []);

  // Filter movie suggestions based on search term
  useEffect(() => {
    if (searchTerm.length > 2) {
      const filteredMovies = allMovies.filter(movie => 
        movie.toLowerCase().includes(searchTerm.toLowerCase())
      ).slice(0, 5);
      
      setMovieSuggestions(filteredMovies);
      setShowSuggestions(true);
      
      // Animate suggestion box
      if (suggestionBoxRef.current && filteredMovies.length > 0) {
        gsap.fromTo(
          suggestionBoxRef.current, 
          { y: -10, opacity: 0 }, 
          { y: 0, opacity: 1, duration: 0.3, ease: "power2.out" }
        );
      }
    } else {
      setMovieSuggestions([]);
      setShowSuggestions(false);
    }
  }, [searchTerm, allMovies]);

  // Get movie details
  const getMovieDetails = async (title) => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_BASE_URL}/movie/${encodeURIComponent(title)}`);
      const data = await response.json();
      
      if (response.ok) {
        setSelectedMovie(data);
      } else {
        setError(data.error || 'Movie not found');
        setSelectedMovie(null);
      }
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while fetching movie details');
      setSelectedMovie(null);
    } finally {
      setLoading(false);
    }
  };


 
  // Get movie recommendations
  const getRecommendations = async (title) => {
    setLoading(true);
    setError('');
    
    try {
      // First get the details of the selected movie
      await getMovieDetails(title);
      
      // Then get recommendations
      const recommendResponse = await fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, count: 6 }),
      });
      
      const recommendData = await recommendResponse.json();
      
      if (recommendResponse.ok) {
        setRecommendedMovies(recommendData.results);
        
        // Animate results
        gsap.fromTo(
          resultsRef.current,
          { opacity: 0, y: 20 },
          { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }
        );
        
        // Animate each movie card with stagger
        gsap.fromTo(
          ".movie-card",
          { scale: 0.9, opacity: 0 },
          { 
            scale: 1, 
            opacity: 1, 
            duration: 0.4, 
            stagger: 0.1, 
            ease: "back.out(1.7)" 
          }
        );
      } else {
        setError(recommendData.error || 'Failed to get recommendations');
        setRecommendedMovies([]);
      }
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while fetching recommendations');
      setRecommendedMovies([]);
    } finally {
      setLoading(false);
    }
  };

  // Handle search form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      getRecommendations(searchTerm);
      setShowSuggestions(false);
    }
  };

  // Handle suggestion selection
  const handleSuggestionClick = (movie) => {
    setSearchTerm(movie);
    getRecommendations(movie);
    setShowSuggestions(false);
  };

  // Handle click on recommended movie
  const handleMovieClick = (movie) => {
    getMovieDetails(movie);
  };

  // Clear search and results
  const handleClearSearch = () => {
    setSearchTerm('');
    setSelectedMovie(null);
    setRecommendedMovies([]);
    setError('');
  };

  // Toggle dark/light mode
  const toggleTheme = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark');
  };

  const addToFavorites = (movie) => {
    if (!favorites.some(fav => fav.title === movie.title)) {
      setFavorites(prev => [...prev, movie]);
      
      // Heart icon animation
      gsap.to(".heart-icon", {
        scale: 1.2,
        duration: 0.3,
        yoyo: true,
        repeat: 1,
        ease: "power2.out"
      });
    }
  };

  // Remove from favorites
  const removeFromFavorites = (movieTitle) => {
    setFavorites(prev => prev.filter(movie => movie.title !== movieTitle));
  };

  return (
    <div className={`min-h-screen flex flex-col ${darkMode ? 'dark' : ''}`}>
      <Header 
        ref={headerRef}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        darkMode={darkMode}
        toggleTheme={toggleTheme}
        favoritesCount={favorites.length}
      />

      <Hero 
        ref={heroRef}
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        handleSubmit={handleSubmit}
        handleClearSearch={handleClearSearch}
        showSuggestions={showSuggestions}
        suggestionBoxRef={suggestionBoxRef}
        movieSuggestions={movieSuggestions}
        handleSuggestionClick={handleSuggestionClick}
        recommendedMovies={recommendedMovies}
      />

      {/* <main ref={resultsRef} className="flex-1 p-6 bg-gray-50 dark:bg-gray-900 w-full">
        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState error={error} setError={setError} />
        ) : (
          <div className="space-y-8 w-full max-w-7xl mx-auto">
            {selectedMovie && <MovieDetails movie={selectedMovie} />}
            
            {recommendedMovies.length > 0 && (
              <MovieList movies={recommendedMovies} onMovieClick={handleMovieClick} />
            )}
          </div>
        )}
      </main> */}
       <main ref={resultsRef} className="flex-1 p-6 bg-gray-50 dark:bg-gray-900 w-full">
        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState error={error} setError={setError} />
        ) : (
          <div className="space-y-8 w-full max-w-7xl mx-auto">
            {activeTab === 'search' && (
              <>
                {selectedMovie && <MovieDetails movie={selectedMovie} onAddToFavorites={addToFavorites} />}
                {recommendedMovies.length > 0 && (
                  <MovieList movies={recommendedMovies} onMovieClick={handleMovieClick} />
                )}
              </>
            )}
            
            {activeTab === 'favorites' && (
              <Favorites 
                favorites={favorites} 
                onRemove={removeFromFavorites}
                onMovieClick={handleMovieClick}
              />
            )}
          </div>
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default App;