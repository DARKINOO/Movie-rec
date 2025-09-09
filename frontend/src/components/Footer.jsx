import React from 'react';
import { Film } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-white dark:bg-gray-800 py-6 shadow-inner w-full">
      <div className="max-w-7xl mx-auto px-4 flex justify-between items-center">
        <div className="flex items-center gap-2 text-red-600">
          <Film size={18} />
          <span className="font-medium">Movieमोक्ष</span>
        </div>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          &copy; 2025 Movieमोक्ष - AI Movie Recommendations
        </p>
      </div>
    </footer>
  );
};

export default Footer;
