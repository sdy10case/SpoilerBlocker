//https://developer.chrome.com/docs/extensions/reference/contextMenus/
markContent = function(word){
    var query = word.selectionText;
    var url = window.location.href;
    alert(url);
    spoiledContent = prompt("You have selected \"" + query + "\". What content is this text spoiling?");
    //Request database url of the page, specific element, timestamp, user role
 };

 viewBlocked = function(word){
    var query = word.selectionText;
    if(confirm("Are you sure you want to view blocked content?"))
        alert(query);
        //Reqeust blocked content?
 }

 unblock = function(word){
     var query = word.selectionText;
     if(confirm("Send a false blocking report?"))
        alert("Report for falsly blocked content has been submitted");
        
 }

chrome.contextMenus.create({
 title: "Mark Content",
 contexts:["selection"], 
 onclick: markContent
});

chrome.contextMenus.create({
    title: "View Blocked Content",
    contexts:["selection"],  
    onclick: viewBlocked
   });

   chrome.contextMenus.create({
    title: "Request to Unblock Content",
    contexts:["selection"], 
    onclick: unblock 
   });
