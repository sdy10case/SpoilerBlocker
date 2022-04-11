const text = document.querySelectorAll('h1, h2, h3, h4, h5, p, li, td, caption, span, a')
//creates a constant variable text that contains all possible text on the document (webpage) and puts it into an array of different text elements
chrome.runtime.sendMessage({ from: "clist", action: [window.location.href] })


chrome.storage.local.get('clist', function (result) {
  var clist = result.clist
  for (elt of text)
    elt.innerHTML = elt.innerHTML.replace(clist[0], clist[1])
})


/*chrome.storage.local.get('key', function(result){
    let x = result.key;
    //runs through the text elements in text and replaces specific things.
    for(elt of text){

        elt.innerHTML = elt.innerHTML.replace(x, "ASDINAODSIA")*/
       // elt.innerHTML = elt.innerHTML.replace("is", "REPLACED")
