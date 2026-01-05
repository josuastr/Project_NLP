document.addEventListener("DOMContentLoaded", () => {
  // --- DOM Elements ---
  const chatMessages = document.getElementById("chatMessages");
  const messageInput = document.getElementById("messageInput");
  const sendButton = document.getElementById("sendButton");

  // --- Event Listeners ---
  sendButton.addEventListener("click", sendMessage);
  messageInput.addEventListener("keypress", handleKeyPress);
  messageInput.addEventListener("input", autoResizeTextarea);

  // --- Functions ---

  // Auto-resize textarea to fit content
  function autoResizeTextarea() {
    this.style.height = "auto";
    this.style.height = `${Math.min(this.scrollHeight, 120)}px`;
  }

  // Send message when Enter is pressed (without Shift)
  function handleKeyPress(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  // Main function to send a message
  function sendMessage() {
    const messageText = messageInput.value.trim();
    if (!messageText) return;

    addMessage(messageText, "user");
    messageInput.value = "";
    autoResizeTextarea.call(messageInput); // Reset height

    fetchBotResponse(messageText);
  }

  // Add a message bubble to the chat
  function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;

    let messageBubbleHtml = "";
    if (sender === "bot") {
      messageBubbleHtml = `
              <div class="bot-avatar">AI</div>
              <div class="message-bubble">${text}</div>
            `;
    } else {
      messageBubbleHtml = `
              <div class="message-bubble">${text}</div>
            `;
    }
    messageDiv.innerHTML = messageBubbleHtml;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
  }

  // Fetch response from the Flask backend
  async function fetchBotResponse(userMessage) {
    showTypingIndicator();
    sendButton.disabled = true;

    try {
      const response = await fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `msg=${encodeURIComponent(userMessage)}`,
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      hideTypingIndicator();
      addMessage(data.response, "bot");
    } catch (error) {
      console.error("Error fetching bot response:", error);
      hideTypingIndicator();
      addMessage("Maaf, terjadi masalah koneksi. Coba lagi nanti.", "bot");
    } finally {
      sendButton.disabled = false;
      messageInput.focus();
    }
  }

  function showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot typing-message";
    typingDiv.innerHTML = `
            <div class="bot-avatar">AI</div>
            <div class="message-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
  }

  function hideTypingIndicator() {
    const typingMessage = document.querySelector(".typing-message");
    if (typingMessage) {
      typingMessage.remove();
    }
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
