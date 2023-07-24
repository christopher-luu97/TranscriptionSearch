export interface AnalyzerData {
  analyzer: AnalyserNode;
  bufferLength: number;
  dataArray: Uint8Array;
}

export interface TranscriptionItem {
  start: number;
  end: number;
  text: string;
  words: Word[];
  start_time_hms: string;
  end_time_hms: string;
}

export interface Word {
  word: string;
  start?: number;
  end?: number;
  score?: number;
}
