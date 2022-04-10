function login() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    chrome.runtime.sendMessage(
        { from: "login", action: [email, password] },
    );
}

document.getElementById('Submit').onclick = login
