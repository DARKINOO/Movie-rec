import React from 'react';
import { Info } from 'lucide-react';

const ErrorState = ({ error, setError }) => {
  return (
    <div className="flex flex-col items-center justify-center h-64">
      <Info size={36} className="text-gray-400 mb-4" />
      <p className="text-gray-600 dark:text-gray-300 mb-6">
        {error}
      </p>
      <button 
        className="px-6 py-2 bg-red-600 hover:bg-red-700 
                 text-white rounded-lg transition-colors"
        onClick={() => setError('')}
      >
        Try Again
      </button>
    </div>
  );
};

export default ErrorState;