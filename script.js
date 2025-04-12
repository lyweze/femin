let audio = document.getElementById('audioPlayer');
let cover = document.getElementById('cover');
let miniCover = document.getElementById('mini-cover');
let playButton = document.getElementById('playButton');
let trackName = document.getElementById('trackName');

const tracks = ['moskva.mp3', 'magnolia.mp3'];
let currenttrack = 0;

const covers = ['moskva.jpeg', 'magnolia.jpeg'];
const names = ['москва', 'magnolia'];


window.addEventListener('keydown', (event) => {
    if (event.keyCode == '32') {
        playOnSpace();
    }
});


function playOnClick() {
    if (!audio.paused){
        audio.pause();
        miniCover.style.cssText = 'width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97); transform: scale(0.94)';
        cover.style.cssText = 'animation: rotate 10s linear infinite; width: 400px; animation-play-state: paused; filter: brightness(80%) grayscale(40%);';
        playButton.innerHTML = '⏵';
    } else {
        audio.play();
        miniCover.style.cssText = 'width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97);';
        cover.style.cssText = 'animation: rotate 10s linear infinite; width: 400px; animation-play-state: running;';
        playButton.innerHTML = '⏸';
    }
}

function changeTrack(pressedBtn) {
    let isPaused = true;

    if (pressedBtn == 'next') {
        currenttrack++;

        if (!audio.paused){
            isPaused = false;
            playOnClick();
        }

        audio.setAttribute('src', ('./music/' + tracks[currenttrack]).toString());
        cover.setAttribute('src', ('./music/covers/' + covers[currenttrack]).toString());
        miniCover.setAttribute('src', ('./music/covers/' + covers[currenttrack]).toString());
        trackName.innerHTML = names[currenttrack].toUpperCase();

        if (!isPaused) {
            playOnClick();
        }
    }
    else {
        currenttrack--;

        if (!audio.paused){
            isPaused = false;
            playOnClick();
        }

        audio.setAttribute('src', ('./music/' + tracks[currenttrack]).toString());
        cover.setAttribute('src', ('./music/covers/' + covers[currenttrack]).toString());
        miniCover.setAttribute('src', ('./music/covers/' + covers[currenttrack]).toString());
        trackName.innerHTML = names[currenttrack].toUpperCase();

        if (!isPaused) {
            playOnClick();
        }
    }
}