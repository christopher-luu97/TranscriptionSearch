import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const Search: React.FC = () => {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };
  const [loading, setLoading] = useState(false);

  const handleSearch = () => {
    setLoading(true); // Set loading state to true
    axios
      .post(`http://127.0.0.1:8000/query_all_transcription/`, { query })
      .then((response) => {
        console.log(response.data.data);
        navigate("/search-results", { state: response.data });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      })
      .finally(() => {
        setLoading(false); // Set loading state back to false when the request completes
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
          className={`px-4 py-2 rounded-md ml-2 ${
            loading ? "bg-blue-500" : "bg-blue-600"
          } text-white`}
          onClick={handleSearch}
          disabled={loading}
        >
          {loading ? (
            <svg
              className="animate-spin h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647zM12 20a8 8 0 100-16 8 8 0 000 16z"
              ></path>
            </svg>
          ) : (
            "Search"
          )}
        </button>
      </div>
    </div>
  );
};
