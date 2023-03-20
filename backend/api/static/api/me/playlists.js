class PlaylistManager {
    constructor(data) {
        this.playlistSelect = document.getElementById('playlistSelect')
        this.previousMode = document.getElementById('previousMode')
        this.titleMode = document.getElementById('titleMode')
        this.nextMode = document.getElementById('nextMode')
        this.bigPlaylistDesc = document.getElementById('bigPlaylistDesc')
        this.songTable = new simpleDatatables.DataTable('#songTable')
        this.playlistData = {}
        for (const i in data.playlists) {
            let playlist = data.playlists[i]
            this.playlistData[playlist.id] = playlist
            const option = document.createElement('option')
            option.value = playlist.id
            option.innerText = playlist.name
            this.playlistSelect.appendChild(option)
        }
        this.playlistSelect.addEventListener('change', () => { this.select(this) })
        this.load_playlist(this)
    }

    select(self) {
        self.load_playlist(self)
    }

    load_playlist(self) {
        const id = self.playlistSelect.value
        this.titleMode.innerText = self.playlistData[id].name
        this.bigPlaylistDesc.innerText = self.playlistData[id].desc
        $.getJSON('/api/me/playlists/playlist?playlist_id=' + id, data => {
            console.log(data)
            this.songTable.destroy()
            this.songTable = new simpleDatatables.DataTable('#songTable', data.chart)
        })
    }
}


$.getJSON('/api/me/playlsits', data => {
    const playlistManager = new PlaylistManager(data)
})