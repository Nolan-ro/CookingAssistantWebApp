function sendMessage() {
    var userInput = document.getElementById("user_input").value;
    if (userInput.trim() === "") return;
    
    var messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += "<div><b>You:</b> " + userInput + "</div>";

    fetch("/get_response", {
        method: "POST",
        body: new URLSearchParams("user_input=" + userInput),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.json())
    .then(data => {
        messagesDiv.innerHTML += "<div><b>Cooking Assistant:</b> " + data.response + "</div>";
        document.getElementById("user_input").value = "";
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}