// import React from 'react';

// const MovieList = ({ movies, onMovieClick }) => {
//   return (
//     <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
//       {movies.map((movie, index) => (
//         <div
//           key={index}
//           className="movie-card bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
//           onClick={() => onMovieClick(movie)}
//         >
//           <h3 className="text-xl font-bold text-gray-900 dark:text-white">{movie}</h3>
//         </div>
//       ))}
//     </div>
//   );
// };

// export default MovieList;

// MovieList.jsx
import { Star } from 'lucide-react';
import React from 'react';

const MovieList = ({ movies, onMovieClick }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white px-4">
        Recommendations
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {movies.map((movie, index) => (
          <div
            key={index}
            className="movie-card bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition-shadow"
            onClick={() => onMovieClick(movie.title)}
          >
            <img
              src={movie.poster || '/placeholder-poster.jpg'}
              alt={movie.title}
              className="w-full h-48 object-cover"
              onError={(e) => {
                e.target.src = '/placeholder-poster.jpg';
                e.target.onerror = null;
              }}
            />
            <div className="p-4">
              <h3 className="text-lg font-bold text-gray-900 dark:text-white truncate">
                {movie.title}
              </h3>
              <div className="flex items-center gap-2 mt-2">
                <Star size={14} className="text-yellow-500" />
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {movie.rating?.toFixed(1) || 'N/A'}/10
                </span>
              </div>
              <div className="flex flex-wrap gap-2 mt-2">
                {movie.genres?.slice(0, 2).map((genre, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 text-xs rounded-full bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300"
                  >
                    {genre}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MovieList;
