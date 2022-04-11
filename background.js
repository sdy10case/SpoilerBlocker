//to do

//privledged users report does not go to request table
import Cookies from js-cookie
chrome.storage.local.set({ 'userId': 9 })
var markMenuId
var unblockMenuId

//Script for request button
request = function (element) {
    chrome.storage.local.get('userId', function (result) {
        var userId = result.userId
        var url = element.pageUrl
        var srcUrl = element.srcUrl
        var highlightedElement = element.selectionText
        if (highlightedElement == null)
            highlightedElement = "an image"
        var type
        if (element.menuItemId == markMenuId) {
            type = "mark"
            isBlocked = "False";
            spoiledContent = prompt("You have selected " + highlightedElement + ". What content is this element spoiling?");
            placehold = prompt("What should be shown instead of the highlighted element?")
        }
        else {
            type = "unblock"
            isBlocked = "True";
            spoiledContent = prompt("Why is the highlighted element falsely blocked?")
            placehold = "ur mom"
        }
        var user_role;
        if (userId != "" && userId != null) {
            if (userId < 20) {
                if (userId < 10) {
                    user_role = "admin"
                }
            }
            else {
                user_role = "moderator"
            }
        }
        else {
            user_role = "base"
        }
        if (user_role == "admin" || user_role == "moderator") {
            sendContent(highlightedElement, url, srcUrl, spoiledContent, isBlocked, user_role);
        }
        else
            sendRequest(userId, highlightedElement, url, srcUrl, spoiledContent, type, placehold, user_role);
    })
};

sendRequest = function (userId, e, u, s, userInput, t, placehold, user_role) {
    //user_role String
    uR = user_role
    //type String
    requestType = t
    //URL String
    url = u
    //identifer String
    if (e == "an image")
        id = s
    else
        id = e
    //reason String
    sC = userInput;
    //isResolved bool
    iR = false;
    fetch('https://reqres.in/api/requests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_role: uR,
            type: requestType,
            URL: url,
            identifier: id,
            placeHolder: placehold,
            spoiledContent: sC,
            isResolved: iR
        })
    })


}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

class makebody {
    constructor(role, u, id, sC, isBlocked) {
        this.user_role = role;
        this.url = u;
        this.identifier = id;
        this.reason = "Reported by mod/admin";
        this.placeholder = sC;
        this.isblocked = isBlocked;
    }
}

sendContent = function (e, u, s, userInput, isBlocked, role) {
    //user_role String
    user_role = role
    //URL String
    url = u
    //identifer String
    if (e == "an image")
        id = s
    else
        id = e
    //reason String
    sC = userInput;
    //isResolved bool
    iR = false;

    const requestinfo = new makebody (user_role, url, id, sC, isBlocked)
    //console.log(requestinfo)
    /*
    requestinfo = {
        user_role: user_role,
        url: url,
        identifier: id,
        reason: "Reported by mod/admin",
        placeholder: sC,
        isblocked: isBlocked
    }
    */
    const requestOptions = {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(requestinfo)
        //mode: 'cors'
    };

    fetch('https://grounded-pager-345917.uc.r.appspot.com/content/', requestOptions)
    /*
    fetch('https://grounded-pager-345917.uc.r.appspot.com')
        
        .then(response => {
            console.log( response.json()) //Convert response to JSON
        })
        
        .then(data => {
            console.log("Data: " + data)//Perform actions with the response data from the view
        })
      */

}

viewBlocked = function (element) {
    var identifer
    if (element.selectionText == null)
        identifer = element.srcUrl
    else
        identifer = element.selectionText
    alert(identifer)
    chrome.storage.local.set('accessDatabase', false)
    chrome.storage.local.get('contentList', function (result) {
        contentList = results.contentList

    })

    var highlightedElement = element.selectionText;
    if (confirm("Are you sure you want to view blocked content?"))
        alert(highlightedElement);
    //Reqeust blocked content?
}

vRequestList = function (element) {
    //Get request 
    var newURL = "http://google.com";
    chrome.tabs.create({ url: newURL });
}

vAccountList = function (element) {
    var newURL = "http://youtube.com";
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
            markMenuId = chrome.contextMenus.create({
                title: "Mark Content",
                contexts: contextsList,
                onclick: request
            })

            unblockMenuId = chrome.contextMenus.create({
                title: "View Blocked Content",
                contexts: contextsList,
                onclick: viewBlocked
            })

            chrome.contextMenus.create({
                title: "Request to Unblock Content",
                contexts: contextsList,
                onclick: request
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
                }
            }
        }
    })
}


chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    /*
    if (message.from && message.from === "clist") {
        toBlock = prompt("What would you like to block?")
        if (toBlock == "") {
            return;
        }
        else {
            replaceVal = "Replaced"
            clist = [toBlock, replaceVal]
            chrome.storage.local.set({ 'clist': clist })
            chrome.storage.local.get('clist', function (result) {
                clist = result.clist
                alert(clist[0] + " will be replaced with " + clist[1])
            })
        }
        
       var url = "https://grounded-pager-345917.uc.r.appspot.com/" + encodeURIComponent(message.action);
       //alert(url)
       fetch('https://grounded-pager-345917.uc.r.appspot.com/')
           .then(response => response.json())
           .then(data => console.log(data))
           .then(response => sendResponse({ farewell: response }))
       
    }
*/
    if (message.from && message.from === "login") {
        credentials = message.action
        alert("Email: " + credentials[0] + ", Password: " + credentials[1])
        if (credentials[0] == "" || credentials[1] == "") {
            alert("Please provide a valid email and password")
            return;
        }

        //Should be a get or put 
        const res = fetch("https://grounded-pager-345917.uc.r.appspot.com/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: credentials[0],
                password: credentials[1]
            })
        })
        const body = res;
        return body;
    }

    else if (message.from && message.from === "register") {
        credentials = message.action
        //make a fetch request to webapp which include generated userID
        const res = fetch("https://grounded-pager-345917.uc.r.appspot.com/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: message.action[0],
                password: message.action[1],
                userID: 5
            })
        })
        const body = res.json();
        alert(body)
        return body;
    }
})

CreateLists()
