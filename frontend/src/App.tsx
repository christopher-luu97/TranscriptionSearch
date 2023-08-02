import React from "react";
import "./App.css";
import { Main } from "./components/Main/Main";
import { Routes, Route } from "react-router-dom";
import { Cards } from "./components/Cards/Cards";
import { IndividualTranscription } from "./components/IndividualTranscription/IndividualTranscription";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Main />} />
      <Route
        path="/IndividualTranscription/:id"
        element={<IndividualTranscription transcriptionData={null} />} // Use the modified Cards component
      />
    </Routes>
  );
};

export default App;
