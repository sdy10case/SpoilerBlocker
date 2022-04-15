const text1 = document.querySelectorAll('h1, h2, h3, h4, h5, p, li, td, caption, span, a')
chrome.storage.local.get('view', function (result) {
    var content = result.view
    console.log(content)
    for (elt of text1)
        elt.innerHTML = elt.innerHTML.replace(content.placeholder, content.identifier)
})
