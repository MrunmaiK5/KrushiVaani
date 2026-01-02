// import { useState } from "react";
// import { Mic, MicOff } from "lucide-react"; // install: npm install lucide-react
// import { startListening } from "../utils/speechHelper";

// export default function VoiceButton({ onSpeechResult }) {
//   const [listening, setListening] = useState(false);

//   const handleStart = () => {
//     setListening(true);
//     startListening(
//       (text) => {
//         onSpeechResult(text);
//         setListening(false);
//       },
//       () => setListening(false)
//     );
//   };

//   return (
//     <button
//       onClick={handleStart}
//       className={`p-3 rounded-full shadow-md transition ${
//         listening ? "bg-red-500 text-white" : "bg-green-500 text-white"
//       }`}
//     >
//       {listening ? <MicOff size={20} /> : <Mic size={20} />}
//     </button>
//   );
// }
import { useState } from "react";
import { Mic, MicOff, Volume2, Square } from "lucide-react"; 
import { startListening } from "../utils/speechHelper";
import axios from "axios";

export default function VoiceButton({ onSpeechResult, textToSpeak, mode = "input" }) {
  const [isListening, setIsListening] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audio, setAudio] = useState(null);

  // --- OUTPUT MODE: AI speaking to the farmer ---
  const handlePlayVoice = async () => {
    if (!textToSpeak) return;

    try {
      setIsPlaying(true);
      // Fetching the .mp3 stream from Sakshi's voice_service
      const response = await axios.post("http://localhost:5000/api/voice/generate", 
        { text: textToSpeak }, 
        { responseType: 'blob' }
      );

      const audioUrl = URL.createObjectURL(response.data);
      const newAudio = new Audio(audioUrl);
      setAudio(newAudio);
      
      newAudio.play();
      newAudio.onended = () => setIsPlaying(false);
    } catch (error) {
      console.error("Audio playback failed:", error);
      setIsPlaying(false);
    }
  };

  const stopAudio = () => {
    if (audio) {
      audio.pause();
      setIsPlaying(false);
    }
  };

  // --- INPUT MODE: Farmer speaking to the app ---
  const handleStartListening = () => {
    setIsListening(true);
    startListening(
      (text) => {
        onSpeechResult(text);
        setIsListening(false);
      },
      () => setIsListening(false)
    );
  };

  // UI for Output (Listening to AI Advice)
  if (mode === "output") {
    return (
      <button
        type="button"
        onClick={isPlaying ? stopAudio : handlePlayVoice}
        className={`flex items-center gap-2 px-4 py-2 rounded-lg shadow transition ${
          isPlaying ? "bg-orange-500 text-white animate-pulse" : "bg-blue-600 text-white hover:bg-blue-700"
        }`}
      >
        {isPlaying ? <Square size={18} /> : <Volume2 size={18} />}
        <span className="font-medium">{isPlaying ? "Stop" : "Advice"}</span>
      </button>
    );
  }

  // UI for Input (Speaking to the Form)
  return (
    <button
      type="button"
      onClick={handleStartListening}
      className={`p-3 rounded-full shadow-md transition ${
        isListening ? "bg-red-500 text-white animate-bounce" : "bg-green-500 text-white hover:bg-green-600"
      }`}
    >
      {isListening ? <MicOff size={20} /> : <Mic size={20} />}
    </button>
  );
}
