/*
chrome.storage.local.clear(function() {
    var error = chrome.runtime.lastError;
    if (error) {
        console.error(error);
    }
});
*/

changePage = function(element){
  if(element.valueOf() == "Register"){
    chrome.browserAction.setPopup({
            popup: "popupRegister.html"
        });
  }
  if(element.valueOf() == "Login"){
    chrome.browserAction.setPopup({
            popup: "popupLogin.html"
        });
  }
}

chrome.storage.local.get('userId', function (result) {
    if (result.userId != null) {
        chrome.browserAction.setPopup({
            popup: "popupLogout.html"
        });
    }
})

markRequest = function (element) {
    chrome.storage.local.get('userId', function (result) {
        chrome.storage.local.get('user_role', function (result2) {
            var userId = result.userId
            var user_role = result2.user_role
            var url = element.pageUrl
            var srcUrl = element.srcUrl
            var highlightedElement = element.selectionText
            chrome.storage.local.set({'highlightedElement': highlightedElement})
            if (highlightedElement == null){
                highlightedElement = "an image"
                if (srcUrl.indexOf("Icons/fullx_monkey") != -1)
                    alert("This image is a placeholder")
                    return true
            }
            type = "create"
            isBlocked = "False";

            chrome.tabs.executeScript({
                file: 'content_script_highlightcheck.js'
            })
            setTimeout(function() { 
            chrome.storage.local.get('mark2', function (result3) {
            if (result3.mark2 == "Bad") {
                spoiledContent = prompt("You have selected " + highlightedElement + ". What content is this element spoiling?");
                if (highlightedElement == "an image") {
                    placehold = "Monkeyyyyy"
                }
                else {
                    placehold = prompt("What should be shown instead of the highlighted element?")
                }
                if (placehold == "" || spoiledContent == "" || spoiledContent == null || spoiledContent == null) {
                    alert("Invalid reasoning")
                    return true;
                }
                if (user_role == "admin" || user_role == "moderator") {
                    sendContent(highlightedElement, url, srcUrl, placehold, isBlocked, user_role, null);
                }
                else
                    sendRequest(userId, highlightedElement, url, srcUrl, spoiledContent, type, placehold, user_role, null);
            }
            else
                alert("You have highlighted a placeholder or already blocked text.")
           
        })}, 250)}
        )
    })
};

reportRequest = function (element) {
    chrome.storage.local.get('userId', function (result1) {
        chrome.storage.local.get('user_role', function (result2) {
            var userId = result1.userId
            var user_role = result2.user_role
            var url = element.pageUrl
            var srcUrl = element.srcUrl
            var highlightedElement = element.selectionText
            var c_id = null;
            if (highlightedElement == "an image")
                identifier = srcUrl
            else
                identifier = highlightedElement
            type = "report"
            chrome.storage.local.get('clist', function (result3) {
                contentList = result3.clist.content
                var blocked = false
                for (let i = 0; i < contentList.length; i++) {
                    if (contentList[i].identifier == identifier) {
                        blocked = contentList[i].isBlocked
                        c_id = contentList[i].c_id
                        placehold = contentList[i].placeholder
                    }
                }
                console.log(placehold)
                if (!blocked) {
                    alert("This content is not currently blocked")
                    return;
                }
                spoiledContent = prompt("Why is the highlighted element falsely blocked?")

                isBlocked = "True"
                if (spoiledContent == "" || spoiledContent == null) {
                    alert("Invalid reasoning")
                    return;
                }
                if (user_role == "admin" || user_role == "moderator") {
                    sendContent(highlightedElement, url, srcUrl, spoiledContent, isBlocked, user_role, c_id);
                }
                else
                    sendRequest(userId, highlightedElement, url, srcUrl, spoiledContent, type, placehold, user_role, c_id);
            })
        })
    })
}

class requestMarkBody {
    constructor(uid, urole, id, r, pH, type, url) {
        this.baseuserid = uid;
        this.user_role = urole;
        this.identifier = id;
        this.reason = r;
        this.placeholder = pH;
        this.type = type;
        this.url = url
    }
}

class requestReportBody {
    constructor(uid, urole, id, r, pH, type, url, c_id) {
        this.baseuserid = uid;
        this.user_role = urole;
        this.identifier = id;
        this.reason = r;
        this.placeholder = pH;
        this.type = type;
        this.url = url;
        this.c = c_id;
    }
}

parseRequestData = function (data) {
    console.log(data.raw)
    if (data.raw == "maxmet") {
        alert("You have met the maximum amount of requests/reports today. Please come back tomorrow!")
        return;
    }
    if (data.raw == "Already Exists") {
        alert("This content has already been marked or reported.")
        return;
    }
    if (data.raw == "Updated Existing request") {
        alert("A request/report has been updated.")
        return;
    }
    else {
        alert("Thank you for submitting a response.")
    }
}

sendRequest = function (userId, e, u, s, sC, requestType, placehold, user_role, c_id) {
    console.log("making request")
    if (e == "an image") {
        id = s
    }
    else
        id = e
    console.log(placehold)
    if (c_id == null)
        var requestinfo = new requestMarkBody(userId, user_role, id, sC, placehold, requestType, u)
    else
        var requestinfo = new requestReportBody(userId, user_role, id, sC, placehold, requestType, u, c_id)
    var requestOptions = {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(requestinfo)
    };
    console.log(requestOptions)
    url = 'https://grounded-pager-345917.uc.r.appspot.com/request/'
    fetch(url, requestOptions)
        .then(response => response.json())
        .then(data => parseRequestData(data))
        .catch(error => console.log(error))
}

class contentBodyMark {
    constructor(role, u, id, pH, isBlocked) {
        this.user_role = role;
        this.url = u;
        this.identifier = id;
        this.reason = "Reported by mod/admin";
        this.placeholder = pH;
        this.isblocked = isBlocked;
    }
}

class contentBodyReport {
    constructor(c_id) {
        this.c_id = c_id
    }
}

sendContent = function (e, url, s, pH, isBlocked, user_role, c_id) {
    //identifier String
    if (e == "an image") {
        id = s
    }
    else
        id = e
    var contentOptions
    if (c_id == null) {
        var contentinfo = new contentBodyMark(user_role, url, id, pH, "True")
        var contentOptions = {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(contentinfo)
        };
    }
    else {
        var contentinfo = new contentBodyReport(c_id)
        var contentOptions = {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(contentinfo)
        };
    }
    fetch('https://grounded-pager-345917.uc.r.appspot.com/content/', contentOptions)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => alert("Server Connection Failure"))
    alert("Thank you for sending content")
}

runView = function (response) {
    chrome.scripting.executeScript({
        files: ['content_script_view.js']
    });
}

viewBlockedPicture = function (element) {
    var monkey = element.srcUrl
    if (monkey.indexOf("Icons/fullx_monkey") == -1) {
        alert("This content is not blocked")
        return;
    }
    var clicked = chrome.extension.getURL(monkey.substring(monkey.indexOf("Icons/fullx_monkey")))
    console.log(clicked)
    if (confirm("Are you sure you want to view blocked content?")) {
        chrome.storage.local.get(clicked, function (result1) {
            var obj = result1;
            oldAlt = obj[clicked]
            if (oldAlt == null) {
                console.log("This image is not blocked")
                return
            }
            console.log("This image is blocked")
            chrome.storage.local.get('clist', function (result2) {
                var contentList = result2.clist.content
                console.log(contentList)
                var something = null
                for (let i = 0; i < contentList.length; i++) {
                    if (contentList[i].placeholder == clicked) {
                        something = contentList[i]
                        console.log("something is something")
                        break
                    }
                }
                if (something == null) {
                    alert("This content is not currently blocked")
                    return;
                }
                chrome.storage.local.set({ 'view': something, 'alt': oldAlt })
                chrome.tabs.executeScript({
                    file: 'content_script_view_image.js'
                })
            });
        })
    }
}

viewBlocked = function (element) {
    var placeholder
    if (element.selectionText == null) {
        return viewBlockedPicture(element)
    }
    else
        placeholder = element.selectionText
    if (confirm("Are you sure you want to view blocked content: " + placeholder)) {
        chrome.storage.local.get('clist', function (result) {
            var contentList = result.clist.content
            var something = null
            for (let i = 0; i < contentList.length; i++) {
                if (contentList[i].placeholder == placeholder) {
                    something = contentList[i]
                    break
                }
            }
            if (something == null) {
                alert("This content is not currently blocked")
                return;
            }
            chrome.storage.local.set({ 'view': something })
            chrome.tabs.executeScript({
                file: 'content_script_view.js'
            });
        })
    }
}

vRequestList = function (element) {
    chrome.storage.local.get('userId', function (result) {
        userId = result.userId
        var newURL = "https://grounded-pager-345917.uc.r.appspot.com/view_request_list/" + userId + "/";
        chrome.tabs.create({ url: newURL });
    })

}

vAccountList = function (element) {
    var newURL = "https://grounded-pager-345917.uc.r.appspot.com/view_user_list";
    chrome.tabs.create({ url: newURL });
}

vContentList = function (element) {
    var newURL = "https://grounded-pager-345917.uc.r.appspot.com/view_content_list/" + element.pageUrl + "/";
    chrome.tabs.update({ url: newURL });
}

function CreateLists() {
    chrome.storage.local.get('user_role', function (result) {
        user_role = result.user_role
        console.log(user_role)
        chrome.storage.local.get('userId', function (result) {
            console.log(result.userId)
        })
        let log = (user_role != "" && user_role != null)
        let mod = (user_role == "moderator")
        let admin = (user_role == "admin")
        contextsList = ["selection", "image"]
        if (log) {
            chrome.contextMenus.create({
                title: "Mark Content",
                contexts: contextsList,
                onclick: markRequest
            })
            chrome.contextMenus.create({
                title: "View Blocked Content",
                contexts: contextsList,
                onclick: viewBlocked
            })
            chrome.contextMenus.create({
                title: "Request to Unblock Content",
                contexts: contextsList,
                onclick: reportRequest
            })
            if (mod || admin) {
                chrome.contextMenus.create({
                    title: "View Request List",
                    contexts: ["all"],
                    onclick: vRequestList
                })
                if (admin) {
                    chrome.contextMenus.create({
                        title: "View Account List",
                        contexts: ["all"],
                        onclick: vAccountList
                    })
                    chrome.contextMenus.create({
                        title: "View Content List",
                        contexts: ["all"],
                        onclick: vContentList
                    })
                }
            }
        }
    })
}

class registerInfo {
    constructor(credentials) {
        this.email = credentials[0],
            this.password = credentials[1],
            this.name = credentials[2],
            this.surname = credentials[3],
            this.user_role = "baseuser"
    }
}

setLoginStore = function (data) {
    if (data.raw == "Wrong Password") {
        alert("Incorrect password, please try again.")
        return;
    }
    chrome.storage.local.set({ 'user_role': data.user_role })
    chrome.storage.local.set({ 'userId': data.userid })
    document.location.reload(true);
    alert("Successful Login")
    chrome.browserAction.setPopup({
        popup: "popupLogout.html"
    });
    CreateLists()
}

parseRegisterResponse = function (data) {
    if (data.raw == "Failure") {
        alert("This email already has an account.")
    }
    else {
        alert("Registration successful, please log in")
    }
}

newURL = function (urlBad) {
    url = urlBad.replaceAll("%3A", ":")
    url = url.replaceAll("%2F", "/")
    return url
}

chrome.runtime.onMessage.addListener(function (message, _sender, sendResponse) {
    if (message.from && message.from === "clist") {
        if (message.action == 'https://www.quackit.com/preview/preview_example_code.cfm') {
            sendResponse("Bad request")
            return true;
        }
        var urlBad = "https://grounded-pager-345917.uc.r.appspot.com/" + encodeURIComponent(message.action) + "/";
        url = newURL(urlBad)
        //alert(url + "\n \n" + urlBad)
        fetch(url)
            .then(response => response.json())
            .then(data => new function () {
                var clist = data
                console.log(clist)
                chrome.storage.local.set({ 'clist': clist })
                console.log("Updated clist")
                sendResponse("Content list was updated")
            })
            .catch(error => console.log(error))
        return true;
    }
    if (message.from && message.from === "login") { //MAKE Wrong Password 
        credentials = message.action
        //credentials = [email, password]
        if (credentials[0] == "" || credentials[1] == "") {
            alert("Please provide a valid email and password")
            return;
        }
        url = "https://grounded-pager-345917.uc.r.appspot.com/login/" + credentials[0] + "/" + credentials[1] + "/"
        fetch(url)
            .then(response => response.json())
            .then(data => setLoginStore(data))
            .catch(error => alert("Invalid login credentials, please try again"))
    }
    if (message.from && message.from === "register") {
        credentials = message.action
        //credentials = ["testbaseuser@email", "123", "Testbase", "User"]
        if (credentials[0] == "" || credentials[1] == "" || credentials[2] == "" || credentials[3] == "") {
            alert("Please provide a valid email, password, name, and last name")
            return;
        }
        const requestinfo = new registerInfo(credentials)
        const requestOptions = {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest' //Necessary to work with request.is_ajax()
            },
            body: JSON.stringify(requestinfo)
        }
        //make a fetch request to webapp which include generated userID
        const res = fetch("https://grounded-pager-345917.uc.r.appspot.com/register/", requestOptions)
            .then(response => response.json())
            .then(data => parseRegisterResponse(data))
            .catch(error => alert("Server Error Please Try Again"))
    }
    if (message.from && message.from == "logout") {
        console.log(message.action)
        chrome.storage.local.set({ 'user_role': null })
        chrome.storage.local.set({ 'userId': null })
        chrome.browserAction.setPopup({
            popup: "popup.html"
        });
        chrome.contextMenus.removeAll()
        console.log("See you later")
        alert("See you later")
    }
	    if (message.from && message.from == "mark") {
        chrome.storage.local.get('highlightedElement', function 						(result2) {
            sendResponse(result2.highlightedElement)})
    }
    if (message.from && message.from == "mark2") {
        chrome.storage.local.set({'mark2': message.action})
    }
    return true;
})

CreateLists()
