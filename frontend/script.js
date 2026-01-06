const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');
const auraGlow = document.getElementById('aura-glow');
const sendBtn = document.getElementById('send-btn');
const inputArea = document.querySelector('.input-area');
const logo = document.querySelector('.logo');

let isGenerating = false;

// Only auto-focus on desktop (not mobile) to prevent keyboard from showing on load
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
if (!isMobile) {
    userInput.focus();
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = userInput.value.trim();

    if (!query || isGenerating) return;

    // 1. Add User Message
    addMessage(query, 'user-message');
    userInput.value = '';
    userInput.disabled = true;
    sendBtn.disabled = true;
    isGenerating = true;

    // 2. Remove Intro if present and move input to bottom
    const intro = document.querySelector('.intro-message');
    if (intro) {
        intro.remove();
        inputArea.classList.add('chat-active');
        logo.classList.add('chat-active');
        chatContainer.classList.add('chat-active');
    }

    // 3. Add AI Placeholder & Activate Aura
    const aiMsgElement = addMessage('', 'ai-message');
    const contentDiv = document.createElement('div');
    aiMsgElement.appendChild(contentDiv);

    // Skeleton loader effect
    contentDiv.innerHTML = '<span class="typing-indicator">...</span>';
    auraGlow.classList.add('active');

    try {
        // 4. Fetch Stream
        const response = await fetch('/chat/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: query })
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullText = '';
        contentDiv.innerHTML = ''; // Clear loading indicator

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            fullText += chunk;

            // basic Markdownish formatting
            contentDiv.innerHTML = formatText(fullText);

            // Auto scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

    } catch (error) {
        console.error('Error:', error);
        contentDiv.innerHTML = 'I apologize, but I encountered a connection error.';
    } finally {
        isGenerating = false;
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
        auraGlow.classList.remove('active');
    }
});

function addMessage(text, className) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;

    if (text) {
        const textNode = document.createElement('div');
        textNode.textContent = text;
        msgDiv.appendChild(textNode);
    }

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return msgDiv;
}

function formatText(text) {
    // Simple formatter for stronger bolding and paragraphs
    // A full markdown library like marked.js could be used here if preferred
    let formatted = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\n\n/g, '<br><br>') // Paragraphs
        .replace(/\n/g, '<br>'); // Line breaks
    return formatted;
}
