import React from "react";
import { Link } from "react-router-dom";

interface SearchResultCardData {
  title: string;
  text: string;
  match: string;
}

interface SearchResultCardsProps {
  searchData: SearchResultCardData[]; // Use the CardData interface for searchData prop
}

// Function to highlight matches from the query
function HighlightedText({ text, match }: { text: string; match: string }) {
  if (!match || !text.toLowerCase().includes(match.toLowerCase())) {
    return <span>{text}</span>;
  }
  const regex = new RegExp(match.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
  const replacedText = text.replace(regex, (matchedPart) => {
    return `<mark class="bg-yellow-300">${matchedPart}</mark>`;
  });

  return <span dangerouslySetInnerHTML={{ __html: replacedText }} />;
}

export function SearchResultCards({ searchData }: SearchResultCardsProps) {
  return (
    <>
      {" "}
      <div className="grid grid-cols-1 gap-10 bg-gray-900">
        {searchData.map((card, index) => (
          <div
            className="flex flex-col justify-between transform transition-transform hover:scale-105 cursor-pointer bg-gray-500 rounded p-4"
            key={index}
            style={{ maxWidth: "800px" }}
          >
            <Link key={index} to={`/IndividualTranscription/${card.title}`}>
              <h1 className="text-2xl font-bold mb-4 text-white text-center my-10">
                {card.title}
              </h1>
              <div className="text-white mt-2relative">
                <p className="relative z-10">
                  <HighlightedText text={card.text} match={card.match} />
                </p>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </>
  );
}
