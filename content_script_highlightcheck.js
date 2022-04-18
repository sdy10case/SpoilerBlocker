var text3 = document.querySelectorAll('h1, h2, h3, h4, h5, p, li, td, caption, span, a')


chrome.runtime.sendMessage({ from: "mark", action: ["None"]}, function (response) {
    let boo = "Bad";
        for(let i = 0; i < text3.length; i++){
            if(text3[i].innerHTML.indexOf(":powderblue") == -1 && text3[i].innerHTML.indexOf(response) != -1){
              boo = "Good"
            chrome.runtime.sendMessage({from: "mark2", action: "Good"})}
        }
    
    if(boo == "Bad")
      chrome.runtime.sendMessage({from: "mark2", action: ["Bad"]})
  
  })
