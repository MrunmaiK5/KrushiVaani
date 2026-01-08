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
import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "नमस्कार! मी कृषीवाणी बोट आहे. मी तुम्हाला कशी मदत करू शकतो?", sender: "bot" }
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  // नवीन मेसेज आल्यावर स्क्रोल खाली नेण्यासाठी
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (input.trim() === "") return;

    const userMessage = { text: input, sender: "user" };
    setMessages(prev => [...prev, userMessage]);
    const userText = input;
    setInput("");

    // बॅकएंड सि्युलेशन (येथे साक्षाचे API येईल)
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        text: "मी तुमच्या प्रश्नावर प्रक्रिया करत आहे. कृपया थोडा वेळ थांबा...", 
        sender: "bot" 
      }]);
    }, 1000);
  };

  return (
    <div className="chatbot-page-wrapper">
      <div className="chatbot-central-card">
        
        {/* चॅटबॉट हेडर - Navy Blue Theme */}
        <div className="chatbot-header">
          <div className="bot-profile">
    
            <div className="bot-details">
              <span className="bot-name">Krushivani AI Bot</span>
              <span className="bot-status">● Online Now</span>
            </div>
          </div>
          <div className="header-actions">
            <button className="close-btn">✕</button>
          </div>
        </div>

        {/* मेसेज एरिया */}
        <div className="chat-body">
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.sender === 'user' ? 'user-align' : 'bot-align'}`}>
              
              <div className={`chat-bubble ${msg.sender}`}>
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* इनपुट एरिया */}
        <div className="chat-footer">
          <input 
            type="text" 
            className="chat-input"
            placeholder="येथे टाईप करा..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <button className="send-btn" onClick={handleSend}>
            <span role="img" aria-label="send">➤</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;