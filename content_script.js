const text = document.querySelectorAll('h1, h2, h3, h4, h5, p, li, td, caption, span, a, code')

const imgs = document.getElementsByTagName('img')
let imgFile = "Icons/fullx_monkey - Copy ("
//creates a constant variable text that contains all possible text on the document (webpage) and puts it into an array of different text elements
//for (elt of imgs)
  //console.log(imgs)

let idAndPH = []

chrome.runtime.sendMessage({ from: "clist", action: [document.location.href] }, function (response) {
  console.log(response)
  chrome.storage.local.get('clist', function (result) {
    var clist = result.clist.content
    console.log(clist)
    for (elt of text) {
      for (let i = 0; i < clist.length; i++) {
        //console.log(clist.length + " " + i)
        //console.log(clist[i].identifer)
        //console.log(clist[i].placeholder)
        //console.log("Replaced: " + clist[i].identifier + " With: " + clist[i].placeholder)
        if (clist[i].isBlocked)
          elt.innerHTML = elt.innerHTML.replace(clist[i].identifier, clist[i].placeholder)
      }
      for (elt of imgs) {
				let j = 2
        for (let i = 0; i < clist.length; i++) {
          if (clist[i].isBlocked && clist[i].identifier == elt.src) {
            let source = imgFile + j + ").png"
            let url = chrome.extension.getURL(source);
            oldAlt = elt.alt
            elt.src = url;
						elt.id = clist[i].placeholder
            source = source.replaceAll(" ", "%20")
            console.log(source)
            
            chrome.storage.local.set({source: oldAlt})
            console.log("Image replaced")
						j++
          }
        }
      }
    }
  })
})


/*chrome.storage.local.get('key', function(result){
    let x = result.key;
    //runs through the text elements in text and replaces specific things.
    for(elt of text){

        elt.innerHTML = elt.innerHTML.replace(x, "ASDINAODSIA")*/
       // elt.innerHTML = elt.innerHTML.replace("is", "REPLACED")
