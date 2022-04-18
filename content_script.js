const text = document.querySelectorAll('h1, h2, h3, h4, h5, p, li, td, caption, span, a, code')
const imgs = document.getElementsByTagName('img')
let imgFile = "Icons/fullx_monkey - Copy ("

chrome.runtime.sendMessage({ from: "clist", action: [document.location.href] }, function (response) {
  console.log(response)
  chrome.storage.local.get('clist', function (result) {
    var clist = result.clist.content
    console.log(clist)
    for (elt of text) {
      for (let i = 0; i < clist.length; i++) {
        if (clist[i].isBlocked)
          elt.innerHTML = elt.innerHTML = elt.innerHTML.replace(clist[i].identifier, '<span style="background-color:powderblue;">' + clist[i].placeholder + '</span> <!--monkey monkey-->')
      }
      for (elt of imgs) {
				let j = 2
        for (let i = 0; i < clist.length; i++) {
          if (clist[i].isBlocked && clist[i].identifier == elt.src) {
            source = imgFile + j + ").png"
            let url = chrome.extension.getURL(source);
            elt.src = url;
            url = url.replaceAll(" ", "%20")
            clist[i].placeholder = url
            oldAlt = elt.alt
            elt.alt = clist[i].reason
            console.log(url)
            console.log(oldAlt)
            var obj = {};
            obj[url] = oldAlt
            chrome.storage.local.set(obj)
            console.log("Image replaced")
						j++
          }
        }
      }
      var packedClist = {"content": clist}
      chrome.storage.local.set({'clist' : packedClist})
    }
  })
})
