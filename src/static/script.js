document.getElementById('chatInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default action to stop it from submitting a form if it was one
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('chatInput');
    const messageText = input.value.trim();
    if (messageText !== '') {
        displayMessage(messageText, 'user'); // 'user' for user messages
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sessionID: 'unique_session_id', query: messageText })
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.response) {
                displayMessage(data.response, 'assistant'); // 'assistant' for assistant messages
            } else {
                displayMessage("No valid response from server", 'error');
            }
            input.value = '';  // Clear input field after sending
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage("Error connecting to server", 'error');
        });
    }
}

function displayMessage(message, type) {
    const chatBox = document.querySelector('.chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);
    messageDiv.innerHTML = `<p>${message}</p>`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}