let userInfo = {};
document.addEventListener('DOMContentLoaded', function() {
    const userForm = document.getElementById('user-info-form');
    const chatSection = document.getElementById('chat-section');
    const chatForm = document.getElementById('chat-form');
    const messagesDiv = document.getElementById('messages');

    userForm.onsubmit = async function(e) {
        e.preventDefault();
        const formData = new FormData(userForm);
        // Send initial user info and images to backend
        const res = await fetch('/api/start_chat', {
            method: 'POST',
            body: formData
        });
        userForm.style.display = 'none';
        chatSection.style.display = '';
        // Get agent's first response
        await loadHistory();
        // Fetch agent response and display
        const chatRes = await fetch('/api/chat_history?bandwidth=high');
        const chatData = await chatRes.json();
        // Find last assistant message and display
        const lastAssistant = chatData.history.reverse().find(m => m.role === 'assistant');
        if (lastAssistant) {
            addMessage('assistant', lastAssistant.response || lastAssistant.content);
        }
    };

    chatForm.onsubmit = async function(e) {
        e.preventDefault();
        const message = chatForm.message.value;
        addMessage('user', message);
        chatForm.message.value = '';
        // Support image upload during chat
        const formData = new FormData();
        formData.append('message', message);
        formData.append('bandwidth', 'high');
        // If user attaches images in chat, send them
        if (chatForm.images && chatForm.images.files.length > 0) {
            for (let i = 0; i < chatForm.images.files.length; i++) {
                formData.append('image' + i, chatForm.images.files[i]);
            }
        }
        const res = await fetch('/api/send_message', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        addMessage('assistant', data.response);
    };

    window.clearChat = async function() {
        await fetch('/api/clear_history', {method: 'POST'});
        messagesDiv.innerHTML = '';
    };

    async function loadHistory() {
        const res = await fetch('/api/chat_history?bandwidth=high');
        const data = await res.json();
        messagesDiv.innerHTML = '';
        data.history.forEach(msg => {
            if (msg.role === 'assistant') {
                addMessage('assistant', msg.response || msg.content);
            } else if (msg.role === 'user') {
                addMessage('user', msg.message || msg.content);
            }
        });
    }

    function addMessage(role, content) {
        const div = document.createElement('div');
        div.className = 'message ' + role;
        const bubble = document.createElement('div');
        bubble.className = 'bubble' + (role === 'assistant' ? ' assistant' : '');
        bubble.textContent = content;
        div.appendChild(bubble);
        messagesDiv.appendChild(div);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
});