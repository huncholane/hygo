$.getJSON('/api/charts/unpopular', data => {
    const dbTable = new simpleDatatables.DataTable('#chartsTable', data)
})