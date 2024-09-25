document.getElementById('chatInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Evitar el comportamiento por defecto de los formularios
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('chatInput');
    const messageText = input.value.trim();
    const progressBar = document.getElementById('progressBar'); // Referencia al círculo de carga

    if (messageText !== '') {
        displayMessage(messageText, 'user'); // Mostrar el mensaje del usuario
        input.value = ''; // Limpiar el campo de entrada
        progressBar.style.visibility = 'visible'; // Mostrar el círculo de carga

        // Enviar el mensaje al servidor con session_id y query
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ session_id: 'unique_session_id', query: messageText }) // session_id en lugar de sessionID
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.response) {
                displayMessage(data.response, 'assistant'); // Mostrar respuesta del asistente
            } else {
                displayMessage("No valid response from server", 'error');
            }
            progressBar.style.visibility = 'hidden'; // Ocultar el círculo de carga
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage("Error connecting to server", 'error');
            progressBar.style.visibility = 'hidden'; // Ocultar el círculo de carga
        });
    }
}

function displayMessage(message, type) {
    const chatBox = document.querySelector('.chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);

    // Crear la etiqueta para 'User' o 'Assistant'
    const label = document.createElement('span');
    label.classList.add('label'); // Estilo para la etiqueta
    label.innerText = type === 'user' ? 'User' : 'Assistant';

    // Contenedor de texto y etiqueta
    const textContainer = document.createElement('div');
    textContainer.classList.add('text-container');
    textContainer.innerHTML = `<p>${message}</p>`;

    // Agregar la etiqueta y el mensaje al contenedor principal
    messageDiv.appendChild(label);
    messageDiv.appendChild(textContainer);

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
