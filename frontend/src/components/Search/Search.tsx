import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const Search: React.FC = () => {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleSearch = () => {
    // Make an API request to your Django backend here
    axios
      .post(`http://127.0.0.1:8000/query_all_transcription/`, { query })
      .then((response) => {
        // Handle the response from the backend
        console.log(response.data.data); // Do something with the data
        navigate("/search-results", { state: response.data });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };
  return (
    <div className="relative">
      <div className="flex items-center justify-center">
        <svg
          className="w-6 h-6 text-gray-500 pointer-events-none mr-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M21 21l-5.2-5.2"
          />
          <circle cx="11" cy="11" r="8" />
        </svg>
        <input
          type="text"
          placeholder="Ask a question...."
          className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 focus:outline-none w-64"
          value={query}
          onChange={handleInputChange}
        />
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded-md ml-2"
          onClick={handleSearch}
        >
          Search
        </button>
      </div>
    </div>
  );
};
