import React, { useEffect } from 'react';
import { HeartOff } from 'lucide-react';
import { gsap } from 'gsap';

const Favorites = ({ favorites, onRemove, onMovieClick }) => {
  useEffect(() => {
    gsap.from(".favorite-item", {
      opacity: 0,
      y: 20,
      stagger: 0.1,
      duration: 0.5,
      ease: "power2.out"
    });
  }, [favorites]);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
        Your Favorite Movies ({favorites.length})
      </h2>
      
      {favorites.length === 0 ? (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          <HeartOff className="mx-auto mb-4" size={40} />
          <p>No favorites added yet. Start adding some movies!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {favorites.map((movie, index) => (
            <div 
              key={index}
              className="favorite-item bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 relative group"
            >
              <h3 
                className="text-xl font-bold text-gray-900 dark:text-white cursor-pointer hover:text-red-600"
                onClick={() => onMovieClick(movie.title)}
              >
                {movie.title}
              </h3>
              
              <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
                <p>Director: {movie.director || 'Unknown'}</p>
                <p>Genres: {movie.genres?.join(', ') || 'Not available'}</p>
              </div>

              <button
                onClick={() => onRemove(movie.title)}
                className="absolute top-4 right-4 text-red-600 hover:text-red-700 opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <HeartOff size={20} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Favorites;