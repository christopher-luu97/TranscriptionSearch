import React from "react";
import "./App.css";
import { Main } from "./components/Main/Main";
import { Footer } from "./components/Footer/Footer";
import { Header } from "./components/Header/Header";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { IndividualTranscription } from "./components/IndividualTranscription/IndividualTranscription";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route
          path="/IndividualTranscription/:id"
          element={<IndividualTranscription />}
        />
      </Routes>
    </Router>
  );
};

export default App;
