import React from "react";
import "./App.css";
import { Main } from "./components/Main/Main";
import { Routes, Route } from "react-router-dom";
import { IndividualTranscription } from "./components/IndividualTranscription/IndividualTranscription";
import SearchResultPage from "./components/SearchTranscription/SearchResultPage";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Main />} />
      <Route
        path="/IndividualTranscription/:id"
        element={<IndividualTranscription transcriptionData={null} />} // Use the modified Cards component
      />
      <Route path="/search-results" element={<SearchResultPage />} />{" "}
      {/* Add the route for the SearchResultPage */}
    </Routes>
  );
};

export default App;
