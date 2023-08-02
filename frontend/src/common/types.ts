export interface TranscriptionItem {
  title: string;
  id_title: string;
  text: string;
  start_time: string;
  end_time: string;
}

export interface TranscriptionOutputProps {
  transcriptionData: TranscriptionItem[] | null;
}
