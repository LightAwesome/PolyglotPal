const socket = io({autoConnect: false});
const joinButton = document.getElementById("join-btn")
const usernameField = document.getElementById("username")
const messageField = document.getElementById("message")
const landingPage = document.getElementById("landing")
const chatPage = document.getElementById("chat")



let clientLang = "";


joinButton.addEventListener("click", () => {
    let username = usernameField.value;
    clientUsername = usernameField.value;
    

    clientLang = document.getElementById("language").value;

    socket.connect();

     socket.on ('connect', () => {
        socket.emit('user_join', {username: username, lang: clientLang});
    })

    chatPage.style.display = "block";
    landingPage.style.display = "none";
})



document.getElementById("message").addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
        let message = messageField.value;
        socket.emit("new_message", message);
        
document.getElementById("message").value = "";
    }
});




socket.on("chat", function(data) {
    let ul = document.getElementById("chat-messages");
    let li = document.createElement("li");
     // Check if the message is from the client or another user
     if (data["username"] === clientUsername) {
        li.classList.add("my-message"); // Apply a class for the client's messages
    } else {
        li.classList.add("other-message"); // Apply a class for other users' messages
    }

    

    
    li.appendChild(document.createTextNode(data["username"] + ": " + data["message"]));
    ul.appendChild(li);
    ul.scrollTop = ul.scrollHeight;



    // // insert the translation here somehow before displaying. My translation code is in app.py, but i want to translate the message here
    // li.appendChild(document.createTextNode(data["username"] + ": " + data["message"]));
    // ul.appendChild(li);
    // ul.scrollTop = ul.scrollHeight;
});

