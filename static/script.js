const inputField = document.getElementById('user-input');
const sendButton = document.getElementById('send-btn');

$('textarea').on({input: function(){
    var totalHeight = $(this).prop('scrollHeight') - parseInt($(this).css('padding-top')) - parseInt($(this).css('padding-bottom'));
    $(this).css({'height':totalHeight});
}
});

// Send button should also send the message
sendButton.addEventListener('click', sendMessage);

function sendMessage() {
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();

    if (message) {
        userMessage = displayUserMessage(message)
        assistantMessage = createAssistantMessage(); //placeholder for a typing animation
        
        //REAL MESSAGE LOGIC USING AJAX AND FLASK
        var xhr = new XMLHttpRequest();
        var url = "/prompt/";

        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("ResponseType", "string");

        var data = JSON.stringify({"prompt": message});

        xhr.onload = function () {
            setMessageContent(assistantMessage, xhr.responseText);
        }

        xhr.send(data);
    }

    function displayUserMessage(message) {
        const inputField = document.getElementById('user-input');
        const chatBox = document.getElementById('chat-box');

        //CHATGPT MESSAGE UI CODE (can't be bothered working with html/css)
        inputField.value = ''; 
        inputField.style.height = '24px'; 
        const userWrapper = document.createElement('div');
        userWrapper.classList.add('message-wrapper', 'user-wrapper');
        const userMessage = document.createElement('div');
        userMessage.textContent = message;
        userMessage.classList.add('message', 'user-message');
        userWrapper.appendChild(userMessage);
        chatBox.appendChild(userWrapper);
        inputField.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;

        return userMessage;
    }

    function createAssistantMessage(message) {
        const chatBox = document.getElementById('chat-box');
        //"thinking" MESSAGE
        const assistantWrapper = document.createElement('div');
        assistantWrapper.classList.add('message-wrapper', 'assistant-wrapper');

        const assistantMessage = document.createElement('div');
        assistantMessage.classList.add('message', 'assistant-message');

        const typingAnim = document.createElement('img');
        typingAnim.classList.add('typing-anim');
        typingAnim.src = "static/assets/typing.gif";

        assistantWrapper.appendChild(assistantMessage);
        chatBox.appendChild(assistantWrapper);
        assistantMessage.appendChild(typingAnim);
        chatBox.scrollTop = chatBox.scrollHeight;

        return assistantMessage;
    }

    function setMessageContent(messageElement, newMessage) {
        messageElement.textContent = newMessage;
    }
}