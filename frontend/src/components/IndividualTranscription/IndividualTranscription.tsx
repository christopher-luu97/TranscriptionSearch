import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export function IndividualTranscription() {
  //   const { id } = useParams(); // Access the "id" parameter from the route URL

  const [transcriptionData, setTranscriptionData] = useState(null);

  //     useEffect(() => {
  //       // Fetch additional data for the individual transcription from the Django backend
  //       fetchTranscriptionData(id).then((data) => {
  //         setTranscriptionData(data);
  //       });
  //     }, [id]);

  if (!transcriptionData) {
    return <div>Loading...</div>;
  }

  return <div>{/* Render the transcription data here */}</div>;
}
