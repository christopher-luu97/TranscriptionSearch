import React from "react";
import { TranscriptionItem } from "../../common/types";

interface TranscriptionOutputProps {
  transcriptionData: TranscriptionItem[];
  maxHeight: number;
  searchWords: string[];
}

const TranscriptionOutput: React.FC<TranscriptionOutputProps> = ({
  transcriptionData,
  maxHeight,
  searchWords,
}) => {
  const highlightText = (text: string): React.ReactNode => {
    if (!searchWords.length) {
      return text;
    }
    const pattern = new RegExp(`(${searchWords.join("|")})`, "gi");
    const parts = text.split(pattern);

    return parts.map((part, index) =>
      searchWords.includes(part.toLowerCase()) ? (
        <span key={index} className="bg-yellow-300">
          {part}
        </span>
      ) : (
        <React.Fragment key={index}>{part}</React.Fragment>
      )
    );
  };

  return (
    <div className="flex-1 bg-gray-300" style={{ width: "100%" }}>
      <div
        className="mb-4 overflow-y-auto"
        style={{ maxHeight: `${maxHeight}px`, width: "100%" }}
      >
        <div className=""></div>
        <ul className="space-y-4">
          {transcriptionData.map((item, index) => (
            <li
              key={index}
              className={`flex flex-col hover:bg-gray-100 p-2 rounded-lg transition-colors duration-200`}
              style={{
                minHeight: "50px",
                flexWrap: "nowrap",
              }}
            >
              <span className="text-gray-500">
                [{item.start_time} &rarr; {item.end_time}]
              </span>
              <p className="mt-2">{highlightText(item.text)}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default TranscriptionOutput;
