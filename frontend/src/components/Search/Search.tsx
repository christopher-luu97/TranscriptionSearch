import React from 'react';

export const Search: React.FC = () => {
    return (
        <div className="relative">
          <input
            type="text"
            placeholder="Search..."
            className="px-4 py-2 pl-10 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 focus:outline-none w-64"
          />
          <svg
            className="w-6 h-6 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 pointer-events-none"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-5.2-5.2" />
            <circle cx="11" cy="11" r="8" />
          </svg>
        </div>
      );
    };