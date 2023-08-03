import { cardData } from "./cardData";
import { Link } from "react-router-dom";

export function Cards() {
  return (
    <>
      <div className="grid grid-cols-4 gap-20 bg-gray-800">
        {cardData.map((card, index) => (
          <Link key={index} to={`/IndividualTranscription/${card.title}`}>
            <div
              className="w-48 h-32 flex flex-col justify-between transform transition-transform hover:scale-105 cursor-pointer"
              key={index}
            >
              <img
                src={`${card.image}`}
                alt={`Card ${index + 1}`}
                className="w-48 h-32" // Set the width and height according to your desired size
              />
              <div className="text-white mt-2relative">
                <p className="relative z-10">{card.description}</p>
                <div className="absolute bottom-0 left-0 w-0 h-2 bg-white transition-width duration-300 ease-in-out group-hover:w-full"></div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </>
  );
}
