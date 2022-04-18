const images = document.getElementsByTagName('img')
chrome.storage.local.get('view', function (result1) {
    chrome.storage.local.get('alt', function (result2) {
        var content = result1.view
        var oldAlt = result2.alt
        console.log("SCRIPT WAS INJECTED")
        console.log(content)
        for (elt of images) {
            console.log(elt)
            if (elt.src.replaceAll(" ", "%20") == content.placeholder) {
                elt.src = content.identifier
                elt.alt = oldAlt
                console.log("IMAGE RE REPLACED")
            }
        }
    })
})