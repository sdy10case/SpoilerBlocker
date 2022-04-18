function login() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    chrome.runtime.sendMessage(
        { from: "login", action: [email, password] },
    );
    window.close()
}

function register() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var name = document.getElementById('name').value;
    var surname = document.getElementById('surname').value;
    chrome.runtime.sendMessage(
        { from: "register", action: [email, password, name, surname] },
    );
    window.close()
}

function logout() {
	chrome.runtime.sendMessage(
        { from: "logout", action: ["I would like to logout"] },
    );
    window.close()
}

try {
    document.getElementById('Login').onclick = login;
} catch (error) {
    console.log(error)
}
try {
	document.getElementById('Register').onclick = register;
} catch (error) {
    console.log(error)
}
try {
	document.getElementById('Logout').onclick = logout;
} catch (error) {
    console.log(error)
}

