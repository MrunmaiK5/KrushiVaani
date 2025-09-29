// Speech-to-Text (STT)
export const startListening = (onResult, onEnd) => {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("Your browser does not support Speech Recognition");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-IN"; // Change to "hi-IN" for Hindi
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    onResult(text);
  };

  recognition.onend = () => {
    if (onEnd) onEnd();
  };

  recognition.start();
  return recognition;
};

// Text-to-Speech (TTS)
export const speakText = (text) => {
  if (!window.speechSynthesis) {
    alert("Your browser does not support Text-to-Speech");
    return;
  }
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-IN";
  window.speechSynthesis.speak(utterance);
};
