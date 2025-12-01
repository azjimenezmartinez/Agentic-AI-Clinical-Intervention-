let userInfo = {};
document.addEventListener('DOMContentLoaded', function() {
    const userForm = document.getElementById('user-info-form');
    const chatSection = document.getElementById('chat-section');
    const chatForm = document.getElementById('chat-form');
    const messagesDiv = document.getElementById('messages');

    userForm.onsubmit = async function(e) {
        e.preventDefault();
        userInfo = {
            name: userForm.name.value,
            age: userForm.age.value,
            sex: userForm.sex.value,
            pain: userForm.pain.value,
            bandwidth: 'medium'
        };
        await fetch('/api/user_info', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(userInfo)
        });
        userForm.style.display = 'none';
        chatSection.style.display = '';
        loadHistory();
    };

    chatForm.onsubmit = async function(e) {
        e.preventDefault();
        const message = chatForm.message.value;
        addMessage('user', message);
        chatForm.message.value = '';
        const res = await fetch('/api/send_message', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message, bandwidth: 'medium'})
        });
        const data = await res.json();
        addMessage('assistant', data.response);
    };

    window.clearChat = async function() {
        await fetch('/api/clear_history', {method: 'POST'});
        messagesDiv.innerHTML = '';
    };

    async function loadHistory() {
        const res = await fetch('/api/chat_history?bandwidth=medium');
        const data = await res.json();
        messagesDiv.innerHTML = '';
        data.history.forEach(msg => addMessage(msg.role, msg.content));
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