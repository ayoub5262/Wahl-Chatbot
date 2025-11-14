const messagesEl = document.getElementById('messages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const suggestionList = document.getElementById('suggestion-list');
const historyList = document.getElementById('history-list');
const newChatBtn = document.getElementById('newChatBtn');

let chatHistory = [];
let previousChats = [];

// Load 15 suggestions from JSON
async function loadSuggestions() {
    try {
        const res = await fetch('/data/faqs.json');
        const data = await res.json();
        const items = data.faq_questions.slice(0, 15);
        suggestionList.innerHTML = '';
        items.forEach(q => {
            const li = document.createElement('li');
            li.textContent = q;
            li.addEventListener('click', () => {
                userInput.value = q;
                sendMessage();
            });
            suggestionList.appendChild(li);
        });
    } catch (err) {
        console.error('Fehler beim Laden der Beispiel-Fragen:', err);
    }
}

// Add message to chat window
function addMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

// Send message to backend
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    chatHistory.push({ user: text, bot: '' });
    userInput.value = '';
    addMessage('Bot schreibt...', 'bot');
    const botPlaceholder = messagesEl.querySelector('.bot-message:last-child');

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_message: text, chat_history: chatHistory.slice(0, -1) })
        });
        const data = await res.json();
        botPlaceholder.textContent = data.bot_response;
        chatHistory[chatHistory.length - 1].bot = data.bot_response;
    } catch (err) {
        botPlaceholder.textContent = 'Fehler beim Server: ' + err;
        console.error(err);
    }
}

// Add current chat to history panel
function saveChatToHistory() {
    if (chatHistory.length === 0) return;
    const summary = chatHistory.map(m => m.user).join(' | ');
    previousChats.push([...chatHistory]);

    const li = document.createElement('li');
    li.textContent = summary.substring(0, 50) + (summary.length > 50 ? '...' : '');
    li.addEventListener('click', () => loadChat(li.textContent));
    historyList.appendChild(li);
}

// Load selected chat
function loadChat(summary) {
    const index = Array.from(historyList.children).findIndex(li => li.textContent === summary);
    if (index >= 0) {
        chatHistory = [...previousChats[index]];
        renderChat();
    }
}

// Render chat messages
function renderChat() {
    messagesEl.innerHTML = '';
    chatHistory.forEach(m => {
        addMessage(m.user, 'user');
        addMessage(m.bot, 'bot');
    });
}

// Start new chat
function startNewChat() {
    saveChatToHistory();
    chatHistory = [];
    messagesEl.innerHTML = '';
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
newChatBtn.addEventListener('click', startNewChat);

loadSuggestions();