import React from "react";
import { TranscriptionItem } from "../../common/types";

interface TranscriptionOutputProps {
  transcriptionData: TranscriptionItem[];
  maxHeight: number;
  onTranscriptionDataUpdate: (
    updatedTranscriptionData: TranscriptionItem[]
  ) => void;
}

const TranscriptionOutput: React.FC<TranscriptionOutputProps> = ({
  transcriptionData,
  maxHeight,
}) => {
  return (
    <div className="flex-1" style={{ width: "100%" }}>
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
                [{item.start_time_hms} &rarr; {item.end_time_hms}]
              </span>
              <p className="mt-2">{item.text}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default TranscriptionOutput;
