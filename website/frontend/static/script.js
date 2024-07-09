document.addEventListener('DOMContentLoaded', () => {
    const chatlog = document.getElementById('chatlog');
    const userInput = document.getElementById('userInput');
    
    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(sender);
        messageElement.innerText = message;
        chatlog.appendChild(messageElement);
        chatlog.scrollTop = chatlog.scrollHeight;
    }
function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(`You: ${message}`, 'user');
            userInput.value = '';
// Simulate chatbot response (Replace with your backend API call)
            setTimeout(() => {
                const response = `Chatbot: Response to "${message}"`;
                addMessage(response, 'bot');
            }, 1000);
        }
    }
document.getElementById('sendButton').addEventListener('click', sendMessage);
});
