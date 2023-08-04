import React, { useState } from "react";
import { Cards } from "../Cards/Cards";
import { Search } from "../Search/Search";
import { Header } from "../Header/Header";
import { Footer } from "../Footer/Footer";
import { useNavigate } from "react-router-dom";

export const Main: React.FC = () => {
  return (
    <main>
      <Header />
      <div className="min-h-screen bg-gray-900">
        <div className="flex items-center justify-center">
          <h1 className="text-5xl font-bold mb-4 text-white text-center my-10">
            Search Your Transcripts
          </h1>
        </div>
        <div className="container mx-auto">
          <div className="mb-4">
            <Search />
          </div>
          <div className="flex items-center justify-between"></div>
          <Cards></Cards>
        </div>
      </div>
      <Footer />
    </main>
  );
};
