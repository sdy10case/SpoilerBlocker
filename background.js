
markRequest = function (element) {
    chrome.storage.local.get('userId', function (result) {
        var userId = result.userId
        console.log(userId)
        var url = element.pageUrl
        var srcUrl = element.srcUrl
        var highlightedElement = element.selectionText
        if (highlightedElement == null)
            highlightedElement = "an image"
        type = "create"
        isBlocked = "False";
        spoiledContent = prompt("You have selected " + highlightedElement + ". What content is this element spoiling?");
        placehold = prompt("What should be shown instead of the highlighted element?")
        //GET USER ROLE SOMEWHERE
        var user_role = "baseuser"
        if (placehold == "" || spoiledContent == "") {
            alert("Invalid reasoning")
            return true;
        }
        if (user_role == "admin" || user_role == "moderator") {
            sendContent(highlightedElement, url, srcUrl, placehold, isBlocked, user_role, null);
        }
        else
            sendRequest(userId, highlightedElement, url, srcUrl, spoiledContent, type, placehold, user_role, null);
    })
};

reportRequest = function (element) {
    chrome.storage.local.get('userId', function (result) {
        var userId = result.userId
        var url = element.pageUrl
        var srcUrl = element.srcUrl
        var highlightedElement = element.selectionText
        var c_id = null;
        if (highlightedElement == "an image")
            identifier = srcUrl
        else
            identifier = highlightedElement
        type = "report"
        chrome.storage.local.get('clist', function (result) {
            contentList = result.clist.content
            var blocked = false
            for (let i = 0; i < contentList.length; i++) {
                if (contentList[i].identifier == identifier) {
                    blocked = contentList[i].isBlocked
                    c_id = contentList[i].c_id
                }
            }
            if (!blocked) {
                alert("This content is not currently blocked")
                return;
            }
            spoiledContent = prompt("Why is the highlighted element falsely blocked?")
            placehold = "ur mom"
            isBlocked = "True"
            var user_role = "admin"

            if (user_role == "admin" || user_role == "moderator") {
                sendContent(highlightedElement, url, srcUrl, spoiledContent, isBlocked, user_role, c_id);
            }
            else
                sendRequest(userId, highlightedElement, url, srcUrl, spoiledContent, type, placehold, user_role, c_id);
        })
    })
}

//add c field from clist for 

//type, ident, role, url, reason, placeholder, isResolved, uid
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

//type, ident, role, url, reason, placeholder, isResolved, uid, c_id
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

sendRequest = function (userId, e, u, s, sC, requestType, placehold, user_role, c_id) {
    //identifier String
    console.log("making request")
    if (e == "an image") {
        id = s
        pH = "Image: " + pH
    }
    else
        id = e
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
    url = 'http://127.0.0.1:8000/request/'
    fetch(url, requestOptions)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error))
    alert("Thank you for sending a request")
}

//user role?
class contentBodyMark { //POST
    constructor(role, u, id, pH, isBlocked) {
        this.user_role = role;
        this.url = u;
        this.identifier = id;
        this.reason = "Reported by mod/admin";
        this.placeholder = pH;
        this.isblocked = isBlocked;
    }
}

class contentBodyReport { //PUT
    constructor(c_id) {
        this.c_id = c_id
    }
}

sendContent = function (e, url, s, pH, isBlocked, user_role, c_id) {
    //identifier String
    if (e == "an image") {
        id = s
        pH = "Image: " + pH
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
        //.then(response => response.json())
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
    var src = monkey.substring(monkey.indexOf("Icons/fullx_monkey"))
    chrome.storage.local.get(src, function (result) {
        oldAlt = result.src
        console.log(oldAlt)
    })
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
            //console.log(contentList)
            var something = null
            for (let i = 0; i < contentList.length; i++) {
                if (contentList[i].placeholder == placeholder) {
                    something = contentList[i]
                    //alert("Clist has been changed")
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
    //Reqeust blocked content?
}

vRequestList = function (element) {
    //Get request 
    var newURL = "http://google.com";
    chrome.tabs.create({ url: newURL });
}

vAccountList = function (element) {
    var newURL = "youtube.com";
    chrome.tabs.create({ url: newURL });
}

vContentList = function (element) {
    var newURL = "https://grounded-pager-345917.uc.r.appspot.com/view_content_list/";
    chrome.tabs.create({ url: newURL });
}

function CreateLists() {
    chrome.storage.local.get('userId', function (result) {
        userId = result.userId
        let log = (userId != "" && userId != null)
        let mod = (userId < 20)
        let admin = (userId < 10)
        //alert("User ID: " + userId + ", Logged in: " + log + ", Mod: " + mod + ", Admin: " + admin)
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

            if (mod) {
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
    chrome.storage.local.set({ 'user_role': data.user_role })
    chrome.storage.local.set({ 'userId': data.baseuserid })
    chrome.storage.local.set({ 'maxmet': data.maxmet })
    alert("Successful Login")
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
        var urlBad = "http://127.0.0.1:8000/" + encodeURIComponent(message.action) + "/";
        url = newURL(urlBad)
        //alert(url + "\n \n" + urlBad)
        fetch(url)
            .then(response => response.json())
            .then(data => new function () {
                const clist = data
                console.log(clist)
                chrome.storage.local.set({ 'clist': clist })
                console.log("Updated clist")
                sendResponse("Content list was updated")
            })
            .catch(error => console.log(error))
        chrome.storage.local.set({ 'accessDatabase': null })
        return true;

    }
    if (message.from && message.from === "login") {
        credentials = message.action
        //credentials = [email, password]
        if (credentials[0] == "" || credentials[1] == "") {
            alert("Please provide a valid email and password")
            return;
        }
        url = "http://127.0.0.1:8000/login/" + credentials[0] + "/" + credentials[1] + "/"
        fetch(url)
            .then(response => response.json())
            .then(data => setLoginStore(data))
            .catch(error => alert("Invalid login credentials, please try again"))
    }
    if (message.from && message.from === "register") {
        //credentials = message.action
        credentials = ["email@email", "123", "Ur", "Mom"]
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
            .then(data => console.log(data))
            .catch(error => alert("Server Error Please Try Again"))
        alert("Registration successful, please log in")
    }
    return true;
})

CreateLists()
