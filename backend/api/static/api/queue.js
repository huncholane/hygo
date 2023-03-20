
function queue(e) {
    let uri = e.getAttribute('uri')
    e.style.color = '#55912E'
    setTimeout(() => {
        e.style.color = 'black'
    }, 3000)
    $.get('/api/queue?uri=' + uri, data => {
        if (data == 'unauthorized') {
            window.location.href = '/login'
        }
    })
}