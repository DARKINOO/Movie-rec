import React from 'react';
import { Loader } from 'lucide-react';

const LoadingState = () => {
  return (
    <div className="flex flex-col items-center justify-center h-64">
      <Loader className="text-red-500 animate-spin mb-4" size={36} />
      <p className="text-gray-500 dark:text-gray-400">
        Finding the perfect movies for you...
      </p>
    </div>
  );
};

export default LoadingState;