$.getJSON('/api/charts', data => {
    const dbTable = new simpleDatatables.DataTable('#chartsTable', data)
})