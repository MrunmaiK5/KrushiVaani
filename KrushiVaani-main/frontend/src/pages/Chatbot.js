// import { useState } from "react";
// import VoiceButton from "../components/VoiceButton";
// import { speakText } from "../utils/speechHelper";
// import { getChatbotResponse } from "../services/chatbotService";

// export default function Chatbot() {
//   const [messages, setMessages] = useState([]);

//   const handleUserMessage = async (text) => {
//     setMessages((prev) => [...prev, { sender: "user", text }]);

//     try {
//       const response = await getChatbotResponse(text);
//       setMessages((prev) => [...prev, { sender: "bot", text: response.answer }]);
//       speakText(response.answer);
//     } catch (error) {
//       console.error(error);
//     }
//   };

//   return (
//     <div className="max-w-xl mx-auto py-8">
//       <h1 className="text-2xl font-bold text-green-700 text-center">🎤 Voice Chatbot</h1>
      
//       <div className="mt-6 space-y-2 p-4 border rounded-lg bg-gray-50 h-80 overflow-y-auto">
//         {messages.map((msg, idx) => (
//           <div
//             key={idx}
//             className={`p-2 rounded ${
//               msg.sender === "user" ? "bg-green-200 text-right" : "bg-gray-200 text-left"
//             }`}
//           >
//             {msg.text}
//           </div>
//         ))}
//       </div>

//       <div className="flex justify-center mt-6">
//         <VoiceButton onSpeechResult={handleUserMessage} />
//       </div>
//     </div>
//   );
// }
