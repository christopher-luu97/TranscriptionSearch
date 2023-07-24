import { useCallback, useEffect, useState } from "react";

// https://dev.to/ssk14/visualizing-audio-as-a-waveform-in-react-o67
// custom hook to get the width and height of the browser window
const useSize = (): [number, number] => {
  // initialize width and height to 0
  const [width, setWidth] = useState<number>(0);
  const [height, setHeight] = useState<number>(0);

  // setSizes callback function to update width and height with current window dimensions
  const setSizes = useCallback(() => {
    setWidth(window.innerWidth);
    setHeight(window.innerHeight);
  }, [setWidth, setHeight]);

  // add event listener for window resize and call setSizes
  useEffect(() => {
    window.addEventListener("resize", setSizes);
    setSizes();
    return () => window.removeEventListener("resize", setSizes);
  }, [setSizes]);

  // return width and height
  return [width, height];
};

export default useSize;
