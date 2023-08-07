import { cardData } from "./cardData";
import { Link } from "react-router-dom";

export function Cards() {
  return (
    <>
      <div className="grid grid-cols-4 gap-28 bg-gray-900">
        {cardData.map((card, index) => (
          <Link key={index} to={`/IndividualTranscription/${card.title}`}>
            <div
              className="w-100 h-32 flex flex-col justify-between transform transition-transform hover:scale-105 cursor-pointer border-2 border-transparent transition-all duration-300"
              key={index}
            >
              <img
                src={`${card.image}`}
                alt={`Card ${index + 1}`}
                className="w-100 h-50" // Set the width and height according to your desired size
              />
              <div className="text-white mt-2 relative">
                <p className="relative z-10 ">{card.description}</p>
                <div className="absolute bottom-0 left-0 w-0 h-2 bg-white transition-width duration-300 ease-in-out group-hover:w-full"></div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </>
  );
}
