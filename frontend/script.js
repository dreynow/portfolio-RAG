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
        // Toggle Tailwind classes for layout shift
        inputArea.classList.add('bottom-5');
        inputArea.classList.remove('bottom-[35vh]');
        logo.classList.add('mt-5');
        logo.classList.remove('mt-[20vh]');
        chatContainer.classList.add('pb-24');
        chatContainer.classList.remove('pb-[140px]');
    }

    // 3. Add AI Placeholder & Activate Aura
    const aiMsgElement = addMessage('', 'ai-message');
    const contentDiv = document.createElement('div');
    aiMsgElement.appendChild(contentDiv);

    // Skeleton loader effect
    contentDiv.innerHTML = '<span class="inline-block animate-typing">...</span>';
    auraGlow.classList.remove('opacity-0');
    auraGlow.classList.add('opacity-100');

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
        auraGlow.classList.remove('opacity-100');
        auraGlow.classList.add('opacity-0');
    }
});

function addMessage(text, type) {
    const msgContainer = document.createElement('div');
    const baseClasses = "max-w-[85%] md:max-w-[80%] flex items-start gap-2 mb-4 animate-slideUp";

    if (type === 'user-message') {
        msgContainer.className = `${baseClasses} self-end flex-row-reverse`;

        const bubble = document.createElement('div');
        bubble.className = "p-3 md:p-4 rounded-xl leading-relaxed text-sm md:text-base bg-gradient-to-br from-[#4a4c4a] to-[#3d3f3d] rounded-br-sm text-white shadow-lg";
        if (text) {
            bubble.innerHTML = formatText(text);
        }
        msgContainer.appendChild(bubble);
        chatContainer.appendChild(msgContainer);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return bubble;
    } else {
        msgContainer.className = `${baseClasses} self-start`;

        // Add AI icon beside the bubble
        const iconDiv = document.createElement('div');
        iconDiv.className = "flex-shrink-0 w-9 h-9 mt-1 border border-accent-color/30 p-1.5 flex items-center justify-center rounded-sm bg-accent-color/5";
        iconDiv.innerHTML = `
            <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full">
                <path d="M25 25V75H50C65 75 75 65 75 50C75 35 65 25 50 25H25Z" stroke="#D2691E" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M45 42C45 36 60 36 60 42C60 48 45 50 45 56C45 62 60 62 60 56" stroke="#D2691E" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        msgContainer.appendChild(iconDiv);

        const bubble = document.createElement('div');
        bubble.className = "p-3 md:p-4 rounded-xl leading-relaxed text-sm md:text-base glass-card rounded-bl-sm flex-1";
        if (text) {
            bubble.innerHTML = formatText(text);
        }
        msgContainer.appendChild(bubble);

        chatContainer.appendChild(msgContainer);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        return bubble;
    }
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
