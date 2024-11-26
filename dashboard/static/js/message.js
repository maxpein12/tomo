// Example: Sending a message
const sendButton = document.querySelector('.send-btn');
const messageInput = document.querySelector('.chat-input input');
const chatMessages = document.querySelector('.chat-messages');

sendButton.addEventListener('click', function() {
    const messageText = messageInput.value;
    if (messageText.trim() !== "") {
        const newMessage = document.createElement('div');
        newMessage.classList.add('message', 'sent');
        newMessage.innerHTML = `<p>${messageText}</p><span class="time">${new Date().toLocaleTimeString()}</span>`;
        chatMessages.appendChild(newMessage);
        messageInput.value = '';
    }
});
