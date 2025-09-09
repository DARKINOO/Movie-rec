import React, { forwardRef, useEffect, useRef } from 'react';
import { Search, X, Film, Zap, Star, Activity } from 'lucide-react';
// Replace Robot, Brain, Sparkles with Zap, Star, Activity which are standard Lucide icons
import gsap from 'gsap';

const Hero = forwardRef(({ 
  searchTerm, 
  setSearchTerm, 
  handleSubmit, 
  handleClearSearch,
  showSuggestions,
  suggestionBoxRef,
  movieSuggestions,
  handleSuggestionClick
}, ref) => {
  const titleRef = useRef(null);
  const taglineRef = useRef(null);
  const formRef = useRef(null);
  const aiIconsRef = useRef(null);

  useEffect(() => {
    // GSAP animations
    const tl = gsap.timeline();
    
    tl.from(titleRef.current, {
      y: -50,
      opacity: 0,
      duration: 0.8,
      ease: "back.out(1.7)"
    })
    .from(taglineRef.current, {
      y: 30,
      opacity: 0,
      duration: 0.6
    }, "-=0.3")
    .from(formRef.current, {
      scale: 0.9,
      opacity: 0,
      duration: 0.7,
      ease: "power2.out"
    }, "-=0.3")
    .from(aiIconsRef.current.children, {
      y: 20,
      opacity: 0,
      stagger: 0.15,
      duration: 0.5
    }, "-=0.5");

    // Subtle floating animation for AI icons
    gsap.to(aiIconsRef.current.children, {
      y: -5,
      duration: 1.5,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
      stagger: 0.2
    });
  }, []);

  return (
    <section 
      ref={ref} 
      className="w-full bg-gradient-to-b from-white to-red-50 dark:from-gray-800 dark:to-gray-900 py-16 overflow-hidden"
    >
      <div className="max-w-4xl mx-auto px-4 text-center relative">
        <h2 
          ref={titleRef}
          className="text-4xl font-bold mb-4 bg-gradient-to-r from-red-600 to-pink-500 text-transparent bg-clip-text"
        >
          Movieमोक्ष <span className="inline-block">✨</span>
        </h2>

        <p 
          ref={taglineRef}
          className="text-lg text-gray-600 dark:text-gray-300 mb-2 max-w-2xl mx-auto"
        >
          Apka intelligent movie साथी, powered by AI जादू
        </p>

        <div 
          ref={aiIconsRef} 
          className="flex justify-center items-center gap-5 mb-8"
        >
          <div className="flex flex-col items-center">
            <Zap size={24} className="text-red-500 mb-1" />
            <span className="text-xs text-gray-500 dark:text-gray-400">Smart AI</span>
          </div>
          <div className="flex flex-col items-center">
            <Star size={24} className="text-yellow-500 mb-1" />
            <span className="text-xs text-gray-500 dark:text-gray-400">जादू Recommendations</span>
          </div>
          <div className="flex flex-col items-center">
            <Activity size={24} className="text-blue-500 mb-1" />
            <span className="text-xs text-gray-500 dark:text-gray-400">Film का दिमाग</span>
          </div>
        </div>
        
        <form 
          ref={formRef}
          onSubmit={handleSubmit} 
          className="relative mx-auto max-w-xl"
        >
          <div className="relative">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Kaunsi film देखनी है aapko? Type here..."
              className="w-full px-6 py-4 rounded-xl border-2 border-gray-200 dark:border-gray-700 
                        bg-white dark:bg-gray-900 text-gray-800 dark:text-white 
                        focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent
                        shadow-lg transition-all duration-300 hover:shadow-xl"
            />
            {searchTerm && (
              <button 
                type="button" 
                className="absolute right-12 top-1/2 -translate-y-1/2 text-gray-400 hover:text-red-500" 
                onClick={handleClearSearch}
              >
                <X size={18} />
              </button>
            )}
            <button 
              type="submit" 
              className="absolute right-4 top-1/2 -translate-y-1/2 text-red-500 hover:scale-110 transition-transform"
            >
              <Search size={20} />
            </button>
          </div>
          
          {showSuggestions && movieSuggestions.length > 0 && (
            <div 
              ref={suggestionBoxRef} 
              className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-gray-800 
                        rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 
                        overflow-hidden z-10"
            >
              <ul>
                {movieSuggestions.map((movie, index) => (
                  <li 
                    key={index} 
                    onClick={() => handleSuggestionClick(movie)}
                    className="flex items-center gap-2 px-6 py-3 cursor-pointer 
                              hover:bg-gray-100 dark:hover:bg-gray-700 
                              text-gray-800 dark:text-gray-200"
                  >
                    <Film size={14} className="text-red-500" />
                    {movie}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </form>

        {/* <div className="mt-6 text-sm text-gray-500 dark:text-gray-400 opacity-75">
          <p>Our AI builds a映画 प्रोफाइल that understands your taste</p>
        </div> */}
      </div>
    </section>
  );
});

export default Hero;