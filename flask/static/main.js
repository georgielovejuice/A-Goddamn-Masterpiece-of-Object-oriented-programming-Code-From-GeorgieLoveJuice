function sendMessage() {
    let userMessage = document.getElementById("userInput").value;
    let chatbox = document.getElementById("chatbox");

    if (userMessage.trim() === "") return;

    chatbox.innerHTML += `<p class="user"><strong>You:</strong> ${userMessage}</p>`;

    fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        chatbox.innerHTML += `<p class="bot"><strong>ChatBot:</strong> ${data.reply}</p>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    });

    document.getElementById("userInput").value = "";
}

function speakText(text) {
    let speech = new SpeechSynthesisUtterance();
    speech.text = text;
    speech.lang = "en-US";  // Adjust language as needed
    speech.rate = 1.0;  // Speed of speech
    speechSynthesis.speak(speech);
}

function startVoiceInput() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        let userMessage = event.results[0][0].transcript;
        document.getElementById("userInput").value = userMessage;
        sendMessage();
    };

    recognition.start();
}