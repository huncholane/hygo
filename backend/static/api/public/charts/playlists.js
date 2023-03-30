$.getJSON('/api/charts/playlists', data => {
    const dbTable = new simpleDatatables.DataTable('#chartsTable', data)
})