function generateSliderHtml(name, min, max) {
    return `<div>
        <div class="values">
            ${name}
            <span id="${name}-range1">
                0
            </span>
            <span> &dash; </span>
            <span id="${name}-range2">
                100
            </span>
        </div>
        <div class="slider-container">
            <div class="slider-track" id="${name}-slider-track"></div>
            <input type="range" min="${min}" max="${max}" value="${min}" step=".01" id="${name}-slider1" name="min-${name}">
            <input type="range" min="${min}" max="${max}" value="${max}" step=".01" id="${name}-slider2" name="max-${name}">
        </div>
    </div>`
}

class DualSlider {
    constructor(name, minGap, min, max) {
        document.getElementById(name).innerHTML = generateSliderHtml(name, min, max)
        this.sliderOne = document.getElementById(name + '-slider1')
        this.sliderTwo = document.getElementById(name + '-slider2')
        this.displayValOne = document.getElementById(name + '-range1')
        this.displayValTwo = document.getElementById(name + '-range2')
        this.minGap = minGap
        this.sliderTrack = document.getElementById(name + "-slider-track")
        this.sliderMaxValue = document.getElementById(name + '-slider1').max
        var self = this
        this.sliderOne.addEventListener('input', e => { self.slideOne() })
        this.sliderTwo.addEventListener('input', e => { self.slideTwo() })
        $(window).on('load', () => {
            self.slideOne()
            self.slideTwo()
        })
    }

    slideOne() {
        if (parseFloat(this.sliderTwo.value) - parseFloat(this.sliderOne.value) <= this.minGap) {
            this.sliderOne.value = parseFloat(this.sliderTwo.value) - this.minGap
        }
        this.displayValOne.textContent = this.sliderOne.value
        this.fillColor()
    }

    slideTwo() {
        if (parseFloat(this.sliderTwo.value) - parseFloat(this.sliderOne.value) <= this.minGap) {
            this.sliderTwo.value = parseFloat(this.sliderOne.value) + this.minGap
        }
        this.displayValTwo.textContent = this.sliderTwo.value
        this.fillColor()
    }

    fillColor() {
        let percent1 = (this.sliderOne.value / this.sliderMaxValue) * 100
        let percent2 = (this.sliderTwo.value / this.sliderMaxValue) * 100
        this.sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #3264fe ${percent1}% , #3264fe ${percent2}%, #dadae5 ${percent2}%)`
    }

    getMin() {
        return parseFloat(this.sliderOne.value)
    }

    getMax() {
        return parseFloat(this.sliderTwo.value)
    }
}

const danceSlider = new DualSlider('danceability', 0, 0, 1)
const valenceSlider = new DualSlider('valence', 0, 0, 1)
const energySlider = new DualSlider('energy', 0, 0, 1)
const tempoSlider = new DualSlider('tempo', 0, 0, 400)
const loudnessSlider = new DualSlider('loudness', 0, 0, 1)
const speechinessSlider = new DualSlider('speechiness', 0, 0, 1)
const instrumentalnessSlider = new DualSlider('instrumentalness', 0, 0, 1)
const livenessSlider = new DualSlider('liveness', 0, 0, 1)
const acousticnessSlider = new DualSlider('acousticness', 0, 0, 1)
const durationSlider = new DualSlider('duration', 0, 0, 1000)
const playlistFriendContainer = document.getElementById('playlist-friend-container')
const friendRows = {}
class FriendRow {
    constructor(friendId, friendUsername) {
        this.friendRowId = `friend-row-${friendId}`
        this.removeFriendButtonId = `remove-friend-button-${friendId}`
        playlistFriendContainer.insertAdjacentHTML('beforeend', `<div class="row pb-2" id="${this.friendRowId}"><div class="col">${friendUsername}</div><div class="col-md-auto"><button type="button" class="btn btn-danger" id="${this.removeFriendButtonId}">Remove</button></div></div>`)
        this.friendRow = document.getElementById(this.friendRowId)
        this.removeFriendButton = document.getElementById(this.removeFriendButtonId)
        this.chosen = true
        let self = this
        this.removeFriendButton.addEventListener('click', e => { self.hide() })
    }

    hide() {
        this.friendRow.classList.add('d-none')
        this.chosen = false
    }

    show() {
        this.friendRow.classList.remove('d-none')
        this.chosen = true
    }
}

const selectPlaylist = document.getElementById('select-playlist')
const deletePlaylistContainer = document.getElementById('delete-playlist-container')
const nameInput = document.getElementById('name-input')
const descInput = document.getElementById('desc-input')
const changeButton = document.getElementById('change-button')
const deletePlaylistButton = document.getElementById('delete-playlist-button')
selectPlaylist.addEventListener('change', e => {
    if (selectPlaylist.value != 'new') {
        deletePlaylistButton.classList.remove('d-none')
        let selection = document.getElementById(selectPlaylist.value)
        for (let fid of selection.dataset.friends.split(',')) {
            if (fid == '') {
                break
            }
            console.log(fid)
            let selection2 = document.getElementById('friend-' + fid)
            console.log(selection2)
            let friendUsername = selection2.dataset.username
            if (!(fid in friendRows)) {
                friendRows[fid] = new FriendRow(fid, friendUsername)
            } else {
                friendRows[fid].show()
            }
        }
        changeButton.classList.remove('btn-success')
        changeButton.classList.add('btn-primary')
        changeButton.innerText = 'Update Playlist'
        nameInput.value = selection.dataset.playlistname
        descInput.value = selection.dataset.playlistdesc
        danceSlider.sliderOne.value = selection.dataset.mindanceability
        danceSlider.sliderTwo.value = selection.dataset.maxdanceability
        danceSlider.slideOne()
        danceSlider.slideTwo()
        valenceSlider.sliderOne.value = selection.dataset.minvalence
        valenceSlider.sliderTwo.value = selection.dataset.maxvalence
        valenceSlider.slideOne()
        valenceSlider.slideTwo()
        energySlider.sliderOne.value = selection.dataset.minenergy
        energySlider.sliderTwo.value = selection.dataset.maxenergy
        energySlider.slideOne()
        energySlider.slideTwo()
        tempoSlider.sliderOne.value = selection.dataset.mintempo
        tempoSlider.sliderTwo.value = selection.dataset.maxtempo
        tempoSlider.slideOne()
        tempoSlider.slideTwo()
        loudnessSlider.sliderOne.value = selection.dataset.minloudness
        loudnessSlider.sliderTwo.value = selection.dataset.maxloudness
        loudnessSlider.slideOne()
        loudnessSlider.slideTwo()
        speechinessSlider.sliderOne.value = selection.dataset.minspeechiness
        speechinessSlider.sliderTwo.value = selection.dataset.maxspeechiness
        speechinessSlider.slideOne()
        speechinessSlider.slideTwo()
        instrumentalnessSlider.sliderOne.value = selection.dataset.mininstrumentalness
        instrumentalnessSlider.sliderTwo.value = selection.dataset.maxinstrumentalness
        instrumentalnessSlider.slideOne()
        instrumentalnessSlider.slideTwo()
        livenessSlider.sliderOne.value = selection.dataset.minliveness
        livenessSlider.sliderTwo.value = selection.dataset.maxliveness
        livenessSlider.slideOne()
        livenessSlider.slideTwo()
        acousticnessSlider.sliderOne.value = selection.dataset.minacousticness
        acousticnessSlider.sliderTwo.value = selection.dataset.maxacousticness
        acousticnessSlider.slideOne()
        acousticnessSlider.slideTwo()
        durationSlider.sliderOne.value = selection.dataset.minduration
        durationSlider.sliderTwo.value = selection.dataset.maxduration
        durationSlider.slideOne()
        durationSlider.slideTwo()
    } else {
        changeButton.classList.remove('btn-primary')
        changeButton.classList.add('btn-success')
        changeButton.innerText = 'Create Playlist'
        deletePlaylistButton.classList.add('d-none')
        nameInput.value = ''
        descInput.value = ''
    }
})


const selectFriend = document.getElementById('select-friend')
const addFriendButton = document.getElementById('add-friend-button')
selectFriend.addEventListener('change', e => {
    if (selectFriend.value == 'none') {
        addFriendButton.classList.add('d-none')
    } else {
        addFriendButton.classList.remove('d-none')
    }
})

addFriendButton.addEventListener('click', e => {
    let selection = document.getElementById('friend-' + selectFriend.value)
    let friendId = selectFriend.value
    let friendRowId = `friend-row-${friendId}`
    let friendUsername = selection.dataset.username
    if (!(friendRowId in friendRows)) {
        friendRows[friendId] = new FriendRow(friendId, friendUsername)
    } else {
        friendRows[friendId].show()
    }
})


deletePlaylistButton.addEventListener('click', e => {
    let submitData = {
        uri: selectPlaylist.value,
        delete: true
    }
    submit(submitData)
})
changeButton.addEventListener('click', e => {
    let chosenFriends = []
    for ([key, val] of Object.entries(friendRows)) {
        if (val.chosen == true) {
            chosenFriends.push(parseInt(key))
        }
    }
    if (nameInput.value == '') {
        alert('Playlist must have a name you silly goose!')
        return
    }
    let submitData = {
        delete: false,
        chosenFriends: chosenFriends,
        uri: selectPlaylist.value,
        name: nameInput.value,
        desc: descInput.value,
        mindanceability: danceSlider.getMin(),
        maxdanceability: danceSlider.getMax(),
        minvalence: valenceSlider.getMin(),
        maxvalence: valenceSlider.getMax(),
        minenergy: energySlider.getMin(),
        maxenergy: energySlider.getMax(),
        mintempo: tempoSlider.getMin(),
        maxtempo: tempoSlider.getMax(),
        minduration: durationSlider.getMin(),
        maxduration: durationSlider.getMax(),
        minloudness: loudnessSlider.getMin(),
        maxloudness: loudnessSlider.getMax(),
        minspeechiness: speechinessSlider.getMin(),
        maxspeechiness: speechinessSlider.getMax(),
        mininstrumentalness: instrumentalnessSlider.getMin(),
        maxinstrumentalness: instrumentalnessSlider.getMax(),
        minliveness: livenessSlider.getMin(),
        maxliveness: livenessSlider.getMax(),
        minacousticness: acousticnessSlider.getMin(),
        maxacousticness: acousticnessSlider.getMax(),
    }
    submit(submitData)
})

function submit(data) {
    let request = new Request(
        '',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            mode: 'same-origin',
            body: JSON.stringify(data)
        },
    )
    fetch(request).then(response => {
        console.log(response)
        window.location.replace('')
    })
}