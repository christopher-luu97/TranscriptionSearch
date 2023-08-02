import { TranscriptionOutputProps } from "../../common/types";
import { DefaultContent } from "./defaultContent";
import TranscriptionOutput from "./TranscriptionOutput";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import { TranscriptionItem } from "../../common/types";

export function IndividualTranscription(props: TranscriptionOutputProps) {
  const { id } = useParams(); // Access the "id" parameter from the route URL
  const [transcriptionData, setTranscriptionData] = useState<
    TranscriptionItem[] | null
  >(null);

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
      })
      .catch((error) => {
        console.error("API Error: ", error);
      });
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
      <div className="min-h-screen bg-gray-900">
        <div className="flex items-center justify-center">
          <h1 className="text-5xl font-bold mb-4 text-white text-center my-10">
            {id}
          </h1>
        </div>
        <div className="container mx-auto">
          <div className="flex items-center justify-between">
            {/* Pass props.transcriptionData to the TranscriptionOutput component */}
            <TranscriptionOutput
              transcriptionData={transcriptionData}
              maxHeight={300}
            />
          </div>
        </div>
      </div>
    </main>
  );
}
