// import React, { useRef } from 'react';
// import { Calendar, Star, Clock, Heart } from 'lucide-react';

// const MovieDetails = ({ movie, onAddToFavorites }) => {
//   const heartRef = useRef(null);

//   const handleAddToFavorites = () => {
//     onAddToFavorites(movie);
    
//     // Button animation
//     gsap.to(heartRef.current, {
//       scale: 1.2,
//       duration: 0.3,
//       yoyo: true,
//       repeat: 1,
//       ease: "power2.out"
//     });
//   };

//   return (
//     <div className="bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-lg flex flex-col lg:flex-row">
//       <div 
//         className="lg:w-80 h-80 lg:h-auto bg-cover bg-center w-full" 
//         style={{ backgroundImage: `url(${movie.poster_path})` }}
//       ></div>
      
//       <div className="p-8 flex flex-col gap-4 flex-1">
//         <h2 className="text-3xl font-bold text-gray-900 dark:text-white">{movie.title}</h2>
//         <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
//                 <p>Director: {movie.director}</p>
//                 <p>Genres: {movie.genres.join(', ')}</p>
//               </div>
        
//         {/* <div className="flex gap-6 text-gray-500 dark:text-gray-400">
//           {movie.release_date && (
//             <span className="flex items-center gap-2">
//               <Calendar size={16} />
//               {new Date(movie.release_date).getFullYear()}
//             </span>
//           )}
//           {movie.vote_average > 0 && (
//             <span className="flex items-center gap-2">
//               <Star size={16} />
//               {movie.vote_average.toFixed(1)}
//             </span>
//           )}
//           {movie.runtime > 0 && (
//             <span className="flex items-center gap-2">
//               <Clock size={16} />
//               {movie.runtime} min
//             </span>
//           )}
//         </div>
        
//         <div className="flex flex-wrap gap-2">
//           {movie.genres && movie.genres.map((genre, index) => (
//             <span 
//               key={index} 
//               className="px-3 py-1 rounded-full text-sm bg-indigo-100 text-indigo-700 
//                          dark:bg-indigo-900/40 dark:text-indigo-300"
//             >
//               {genre.name}
//             </span>
//           ))}
//         </div> */}
        
//         <p className="text-gray-600 dark:text-gray-300 leading-relaxed my-4 max-h-40 overflow-y-auto">
//           {movie.overview}
//         </p>
        
//         <button 
//         ref={heartRef}
//         onClick={handleAddToFavorites}
//         className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg transition-all w-fit mt-auto"
//       >
//         <Heart size={16} className="heart-icon" />
//         Add to Favorites
//       </button>
//       </div>
//     </div>
//   );
// };

// export default MovieDetails;

import React from 'react';
import { Calendar, Star, Heart } from 'lucide-react';

const MovieDetails = ({ movie, onAddToFavorites }) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-lg flex flex-col lg:flex-row">
      <img 
        src={movie.poster || '/placeholder-poster.jpg'}
        alt={movie.title}
        className="lg:w-80 h-80 lg:h-auto object-cover w-full"
        onError={(e) => {
          e.target.src = '/placeholder-poster.jpg';
          e.target.onerror = null;
        }}
      />
      
      <div className="p-8 flex flex-col gap-4 flex-1">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">{movie.title}</h2>
        
        <div className="flex gap-6 text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-2">
            <Star size={16} className="text-yellow-500" />
            <span>{movie.rating?.toFixed(1) || 'N/A'}/10</span>
          </div>
          
          {movie.release_date && (
            <span className="flex items-center gap-2">
              <Calendar size={16} />
              {new Date(movie.release_date).getFullYear()}
            </span>
          )}
        </div>

        <div className="flex flex-wrap gap-2">
          {movie.genres?.map((genre, index) => (
            <span 
              key={index}
              className="px-3 py-1 rounded-full text-sm bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300"
            >
              {genre}
            </span>
          ))}
        </div>

        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
          {movie.overview || 'No overview available'}
        </p>

        <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
          <p>Director: {movie.director || 'Unknown'}</p>
          <p>Cast: {movie.cast?.join(', ') || 'Not available'}</p>
        </div>

        <button 
          onClick={() => onAddToFavorites(movie)}
          className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg transition-colors w-fit mt-auto"
        >
          <Heart size={16} />
          Add to Favorites
        </button>
      </div>
    </div>
  );
};

export default MovieDetails;