import { useRef, useEffect } from "react";
import useSize from "./useSize";
import { AnalyzerData } from "../common/types";

interface WaveFormProps {
  analyzerData: AnalyzerData;
}

// https://dev.to/ssk14/visualizing-audio-as-a-waveform-in-react-o67
function animateBars(
  analyser: AnalyserNode,
  canvas: HTMLCanvasElement,
  canvasCtx: CanvasRenderingContext2D,
  dataArray: Uint8Array,
  bufferLength: number
) {
  analyser.getByteFrequencyData(dataArray);

  canvasCtx.fillStyle = "#000";

  const HEIGHT = canvas.height;
  const WIDTH = canvas.width;

  let barWidth = Math.ceil(WIDTH / bufferLength) * 2.5;
  let barHeight;
  let x = 0;

  for (var i = 0; i < bufferLength; i++) {
    barHeight = (dataArray[i] / 255) * HEIGHT;
    const blueShade = Math.floor((dataArray[i] / 255) * 5); // generate a shade of blue based on the audio input
    const blueHex = ["#61dafb", "#5ac8fa", "#50b6f5", "#419de6", "#20232a"][
      blueShade
    ]; // use react logo blue shades
    canvasCtx.fillStyle = blueHex;
    canvasCtx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);

    x += barWidth + 1;
  }
}

const WaveForm = ({ analyzerData }: WaveFormProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { dataArray, analyzer, bufferLength } = analyzerData;
  const [width, height] = useSize();

  const draw = (
    dataArray: Uint8Array,
    analyzer: AnalyserNode,
    bufferLength: number
  ) => {
    const canvas = canvasRef.current;
    if (!canvas || !analyzer) return;
    const canvasCtx = canvas.getContext("2d") as CanvasRenderingContext2D;

    const animate = () => {
      requestAnimationFrame(animate);
      // eslint-disable-next-line no-self-assign
      canvas.width = canvas.width;
      canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
      animateBars(analyzer, canvas, canvasCtx, dataArray, bufferLength);
    };

    animate();
  };

  useEffect(() => {
    draw(dataArray, analyzer, bufferLength);
  }, [dataArray, analyzer, bufferLength]);

  return (
    <div
      style={{
        height: "50%",
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        marginBottom: "20px",
        backgroundColor: "#333", // Add the desired darker background color
        borderRadius: "10px", // Add the desired border radius for rounded corners
      }}
    >
      <canvas
        style={{
          width: "100%",
          height: "100%",
          maxWidth: "100%",
          maxHeight: "100%",
        }}
        ref={canvasRef}
        width={width}
        height={height}
      />
    </div>
  );
};

export default WaveForm;
