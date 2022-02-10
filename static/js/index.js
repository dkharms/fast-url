function short_url(url) {
    fetch('https://fast-url.deta.dev/short', {
        method: 'POST', headers: {
            'Accept': 'application/json', 'Content-Type': 'application/json',
        }, body: JSON.stringify({"url": url})
    }).then((response) => {
        return response.json()
    }).then((data) => {
        document.getElementById('short-url').value = data['url']
    })
}
