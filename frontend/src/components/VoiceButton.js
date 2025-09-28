import { useState } from "react";
import { Mic, MicOff } from "lucide-react"; // install: npm install lucide-react
import { startListening } from "../utils/speechHelper";

export default function VoiceButton({ onSpeechResult }) {
  const [listening, setListening] = useState(false);

  const handleStart = () => {
    setListening(true);
    startListening(
      (text) => {
        onSpeechResult(text);
        setListening(false);
      },
      () => setListening(false)
    );
  };

  return (
    <button
      onClick={handleStart}
      className={`p-3 rounded-full shadow-md transition ${
        listening ? "bg-red-500 text-white" : "bg-green-500 text-white"
      }`}
    >
      {listening ? <MicOff size={20} /> : <Mic size={20} />}
    </button>
  );
}
