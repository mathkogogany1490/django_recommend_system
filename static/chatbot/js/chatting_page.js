function sendMessage() {
    const chatInput = document.getElementById("chat-input");
    const chatBox = document.getElementById("chat-box");

    if (chatInput.value.trim() !== "") {
      // 사용자의 메시지를 채팅창에 추가
      const userMessage = document.createElement("div");
      userMessage.className = "user-message";
      userMessage.textContent = chatInput.value;
      chatBox.appendChild(userMessage);

      // 서버에 메시지 전송
      fetch("/chatbot/api/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ message: chatInput.value }),
      })
      .then((response) => response.json())
      .then((data) => {
        // 약간의 지연을 두고 서버의 응답을 추가
        setTimeout(() => {
          const botMessage = document.createElement("div");
          botMessage.className = "bot-message";
          botMessage.textContent = data.reply;
          chatBox.appendChild(botMessage);

          // 채팅창 자동 스크롤
          chatBox.scrollTop = chatBox.scrollHeight;
        }, 500); // 1초 지연
      });

      // 입력 필드 비우기
      chatInput.value = "";
    }
}

// Enter 키를 감지하는 함수
function checkEnter(event) {
    if (event.keyCode === 13) {  // Enter 키는 keyCode 13
        sendMessage();  // 메시지 전송
    }
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}