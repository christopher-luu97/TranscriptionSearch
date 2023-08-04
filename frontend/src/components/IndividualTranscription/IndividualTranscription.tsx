import { TranscriptionOutputProps } from "../../common/types";
import { DefaultContent } from "./defaultContent";
import TranscriptionOutput from "./TranscriptionOutput";
import { useParams } from "react-router-dom";
import { useState, useEffect, useMemo } from "react";
import axios from "axios";
import { TranscriptionItem } from "../../common/types";
import { Header } from "../Header/Header";
import { Footer } from "../Footer/Footer";

export function IndividualTranscription(props: TranscriptionOutputProps) {
  const { id } = useParams(); // Access the "id" parameter from the route URL
  const [transcriptionData, setTranscriptionData] = useState<
    TranscriptionItem[] | null
  >(null);
  const [originalTranscriptionData, setOriginalTranscriptionData] = useState<
    TranscriptionItem[] | null
  >(null);
  const [wordSearch, setWordSearch] = useState<string>("");
  const [timeSearch, setTimeSearch] = useState<string>("");

  useEffect(() => {
    fetchTranscriptionData();
  }, []);

  const fetchTranscriptionData = () => {
    // send card metadata to DJANGO backend here
    // navigate to associated card page
    const apiEndpoint = "http://127.0.0.1:8000/individual_transcription/";
    const dataToSend = { title: id };
    console.log("ID", id);
    axios
      .post(apiEndpoint, dataToSend)
      .then((response) => {
        console.log("API Response: ", response.data);
        setTranscriptionData(response.data.data);
        console.log(response.data.data);
        setOriginalTranscriptionData(response.data.data); // Store the original data
      })
      .catch((error) => {
        console.error("API Error: ", error);
      });
  };

  const filteredData = useMemo(() => {
    if (!transcriptionData) {
      return null;
    }

    // If both search fields are empty, show the original data
    if (!wordSearch && !timeSearch) {
      return transcriptionData;
    }

    let dataCopy = [...transcriptionData];

    // Apply word search filter
    if (wordSearch) {
      dataCopy = dataCopy.filter((item) =>
        item.text.toLowerCase().includes(wordSearch.toLowerCase())
      );
    }

    // Apply time search filter to work when start_time <= input <= end_time
    if (timeSearch) {
      const timeSearchParts = timeSearch.split(":");
      if (timeSearchParts.length === 3) {
        const [hours, minutes, seconds] = timeSearchParts;
        const timeSearchMs =
          parseInt(hours) * 3600 + parseInt(minutes) * 60 + parseInt(seconds);

        dataCopy = dataCopy.filter((item) => {
          const startTimeParts = item.start_time.split(":");
          const endTimeParts = item.end_time.split(":");

          if (startTimeParts.length === 3 && endTimeParts.length === 3) {
            const startTimeMs =
              parseInt(startTimeParts[0]) * 3600 +
              parseInt(startTimeParts[1]) * 60 +
              parseInt(startTimeParts[2]);
            const endTimeMs =
              parseInt(endTimeParts[0]) * 3600 +
              parseInt(endTimeParts[1]) * 60 +
              parseInt(endTimeParts[2]);

            const matchesTimeSearch =
              timeSearchMs >= startTimeMs && timeSearchMs <= endTimeMs;
            return matchesTimeSearch;
          }

          return false;
        });
      }
    }

    return dataCopy;
  }, [transcriptionData, wordSearch, timeSearch]);

  const handleWordSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const lowercaseSearchTerm = e.target.value.toLowerCase();
    setWordSearch(lowercaseSearchTerm);
  };

  const handleTimeSearchChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const inputValue = event.target.value;
    // Remove any non-digit characters from the input value
    const cleanedValue = inputValue.replace(/[^\d]/g, "");

    // Limit the cleaned value to a maximum length of 6 characters (HHMMSS)
    const limitedValue = cleanedValue.slice(0, 6);

    // Format the limited value into the HH:MM:SS format or HH:MM format or HH format
    let formattedValue = "";
    if (limitedValue.length > 4) {
      formattedValue = limitedValue.replace(
        /^(\d{0,2})(\d{0,2})(\d{0,2})$/,
        (match, hour, minute, second) =>
          `${hour ? hour + ":" : ""}${minute ? minute + ":" : ""}${second}`
      );
    } else if (limitedValue.length > 2) {
      formattedValue = limitedValue.replace(
        /^(\d{0,2})(\d{0,2})$/,
        (match, hour, minute) => `${hour ? hour + ":" : ""}${minute}`
      );
    } else {
      formattedValue = limitedValue;
    }
    setTimeSearch(formattedValue);
  };

  if (!transcriptionData) {
    return (
      <main>
        <DefaultContent />
      </main>
    );
  }

  return (
    <main>
      <Header />
      <div className="min-h-screen bg-gray-900">
        <div className="flex items-center justify-center">
          <h1 className="text-5xl font-bold mb-4 text-white text-center my-10">
            {id}
          </h1>
        </div>
        <div className="container mx-auto flex">
          <div className="w-1/2 pr-2">
            <input
              type="text"
              className="py-2 px-4 bg-gray-200 text-gray-700 rounded w-full"
              placeholder="Search by words"
              value={wordSearch}
              onChange={handleWordSearchChange}
            />
          </div>
          <div className="w-1/2 pl-2">
            <input
              type="text"
              className="py-2 px-4 bg-gray-200 text-gray-700 rounded w-full"
              placeholder="Search by time"
              value={timeSearch}
              onChange={handleTimeSearchChange}
            />
          </div>
        </div>
        <div className="py-2"></div>
        <div className="container mx-auto flex">
          <div className="flex items-center justify-between">
            {filteredData ? (
              <TranscriptionOutput
                transcriptionData={filteredData} // Use the filteredData in TranscriptionOutput
                maxHeight={500}
                searchWords={[wordSearch]}
              />
            ) : (
              <DefaultContent />
            )}
          </div>
        </div>
      </div>
      <Footer />
    </main>
  );
}
