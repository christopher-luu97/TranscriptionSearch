import React, { useState } from "react";
import axios from "axios";
import { TranscriptionItem } from "../common/types";

interface DownloadDropdownProps {
  transcriptionData: TranscriptionItem[] | null;
  fileName?: string;
}

const DownloadDropdown: React.FC<DownloadDropdownProps> = ({
  transcriptionData,
  fileName,
}) => {
  const [selectedFormat, setSelectedFormat] = useState<string>("");

  const handleFormatChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedFormat(e.target.value);
  };

  const handleDownload = () => {
    if (selectedFormat) {
      // Create a new FormData instance
      const formData = new FormData();
      formData.append("file_name", fileName ?? "");
      formData.append("data", JSON.stringify(transcriptionData));
      formData.append("format", selectedFormat);

      // Uncomment to see the data posted to the server
      // console.log({
      //   data: JSON.stringify(transcriptionData),
      //   format: selectedFormat,
      // });
      axios
        .post(
          "http://localhost:8000/backend/transcription_webapp/download/",
          formData,
          { responseType: "blob" } // Set the response type to 'blob' as we expecting binary
        )
        .then((response) => {
          // Handle the response from the Django backend API
          // For this example, we will assume the response contains the file URL
          const fileUrl = URL.createObjectURL(response.data);
          const downloadLink = document.createElement("a");
          downloadLink.href = fileUrl;
          const nameWithoutExtension =
            fileName?.split(".")[0] ?? "transcription";

          // Set the filename using the input filename and selected extension
          downloadLink.download = fileName
            ? `${nameWithoutExtension}.${selectedFormat}`
            : `transcription.${selectedFormat}`;

          downloadLink.click();
        })
        .catch((error) => {
          // Handle any errors that occur during the request
          console.error(error);
        });
    }
  };

  return (
    <div>
      <select
        value={selectedFormat}
        onChange={handleFormatChange}
        className="mr-2 py-2 px-4 bg-gray-200 text-gray-700 rounded"
      >
        <option value="">Select Format</option>
        <option value="csv">CSV</option>
        <option value="txt">TXT</option>
        <option value="srt">SRT</option>
        <option value="vtt">VTT</option>
      </select>
      <button
        onClick={handleDownload}
        className="py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white rounded"
        disabled={!selectedFormat}
      >
        Download
      </button>
    </div>
  );
};

export default DownloadDropdown;
