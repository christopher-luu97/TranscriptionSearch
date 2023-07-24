import React, {
  useState,
  ChangeEvent,
  KeyboardEvent,
  useRef,
  useEffect,
} from "react";
import { TranscriptionItem } from "../common/types";

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
  onTranscriptionDataUpdate,
}) => {
  const [editableIndex, setEditableIndex] = useState<number | null>(null);
  const [editedText, setEditedText] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);
  const divRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (editableIndex !== null && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.selectionStart = inputRef.current.value.length;
      inputRef.current.selectionEnd = inputRef.current.value.length;
    }
  }, [editableIndex]);

  useEffect(() => {
    if (divRef.current) {
      divRef.current.style.width = divRef.current.offsetWidth + "px";
    }
  }, []);

  const handleDoubleClick = (index: number) => {
    setEditableIndex(index);
    setEditedText(transcriptionData[index].text);
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEditedText(e.target.value);
  };

  const handleBlur = () => {
    finalizeChanges();
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      finalizeChanges();
    }
  };

  const finalizeChanges = () => {
    if (editableIndex !== null) {
      const updatedTranscriptionData = [...transcriptionData];
      updatedTranscriptionData[editableIndex].text = editedText;
      onTranscriptionDataUpdate(updatedTranscriptionData);

      setEditableIndex(null);
    }
  };

  return (
    <div className="flex-1" style={{ width: "100%" }}>
      <div
        ref={divRef}
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
              onDoubleClick={() => handleDoubleClick(index)}
            >
              <span className="text-gray-500">
                [{item.start_time_hms} &rarr; {item.end_time_hms}]
              </span>
              {editableIndex === index ? (
                <div style={{ width: "100%" }}>
                  <input
                    type="text"
                    value={editedText}
                    onChange={handleInputChange}
                    onBlur={handleBlur}
                    onKeyDown={handleKeyDown}
                    className="mt-2 border border-gray-300 rounded-md p-2 w-full"
                    autoFocus
                    ref={inputRef}
                  />
                </div>
              ) : (
                <p className="mt-2">{item.text}</p>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default TranscriptionOutput;
