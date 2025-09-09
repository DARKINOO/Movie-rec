import React, { forwardRef } from 'react';
import { Film, Search, TrendingUp, Heart } from 'lucide-react';

const Header = forwardRef(({ activeTab, setActiveTab, darkMode, toggleTheme, favoritesCount }, ref) => {
  return (
    <header 
      ref={ref} 
      className="sticky top-0 z-100 bg-white dark:bg-gray-800 shadow-md w-full"
    >
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Film size={28} className="text-red-600" />
          <h1 className="text-2xl font-bold bg-gradient-to-r from-red-600 to-pink-500 text-transparent bg-clip-text">
          Movieमोक्ष
          </h1>
        </div>
        
        <nav className="flex gap-4">
          <button 
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              activeTab === 'search' 
                ? 'bg-red-100 text-red-600 dark:bg-red-900/30' 
                : 'text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400'
            }`}
            onClick={() => setActiveTab('search')}
          >
            <Search size={18} />
            <span>Search</span>
          </button>
          <button 
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              activeTab === 'trending' 
                ? 'bg-red-100 text-red-600 dark:bg-red-900/30' 
                : 'text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400'
            }`}
            onClick={() => setActiveTab('trending')}
          >
            <TrendingUp size={18} />
            <span>Trending</span>
          </button>
          <button 
        className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
          activeTab === 'favorites' 
            ? 'bg-red-100 text-red-600 dark:bg-red-900/30' 
            : 'text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400'
        }`}
        onClick={() => setActiveTab('favorites')}
      >
        <div className="relative">
          <Heart size={18} />
          {favoritesCount > 0 && (
            <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
              {favoritesCount}
            </span>
          )}
        </div>
        <span>Favorites</span>
      </button>
        </nav>
        
        {/* <button 
          className="text-2xl hover:rotate-12 transition-transform" 
          onClick={toggleTheme}
        >
          {darkMode ? '☀️' : '🌙'}
        </button> */}
      </div>
    </header>
  );
});

export default Header;