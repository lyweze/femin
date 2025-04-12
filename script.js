let audio = document.getElementById('audioPlayer');
let cover = document.getElementById('cover');
let miniCover = document.getElementById('mini-cover');
let playButton = document.getElementById('playButton');
let trackName = document.getElementById('trackName');
let playerTrackName = document.getElementById('playerTrackName');
let progressBar = document.getElementById('progressBar');
let volume = document.getElementById('volume');
let rangeProgress = document.getElementById('rangeProgress');
let rangeVolume = document.getElementById('rangeVolume');

const tracks = ['moskva.mp3', 'casino.mp3','magnolia.mp3'];
let currenttrack = 0;

const covers = ['moskva.jpeg', 'casino.jpeg', 'magnolia.jpeg'];
const names = ['москва', 'casino','magnolia'];


window.addEventListener('keydown', (event) => {
    switch (event.keyCode){
        case 39:audio.currentTime += 5; progressBar.setAttribute('value', audio.currentTime.toString()); break;
        case 37: audio.currentTime -= 5; progressBar.setAttribute('value', audio.currentTime.toString()); break;
        case 32: playOnClick(); break;
        case 38: if ((audio.volume + 0.1) > 1){audio.volume = 1;}else{audio.volume += 0.1;}; volume.setAttribute('value', audio.volume.toString()); break;
        case 40: audio.volume -= 0.1; volume.setAttribute('value', audio.volume.toString()); break;
    }
});

rangeProgress.addEventListener('input', () => {
    isInput = true;
    audio.currentTime =  (audio.duration - 0.2) * (rangeProgress.value/100);
    progressBar.setAttribute('max', (audio.duration).toString());
    progressBar.setAttribute('value', audio.currentTime.toString());
    progressBar.style.scale = '1.01';
    progressBar.style.boxShadow = '0 0 10px rgba(128, 52, 163, 0.35)';
});
rangeProgress.addEventListener('mouseup', () => {
    isInput = false;
    progressBar.style.scale = '1';
    progressBar.style.boxShadow = '';
    rangeProgress.blur();
});

rangeVolume.addEventListener('input', () => {
    audio.volume =  rangeVolume.value;
    volume.setAttribute('value', audio.volume.toString());
    volume.style.scale = '1.01';
    volume.style.height = '30px';
    volume.style.boxShadow = '0 0 20px rgba(128, 52, 163, 0.35)';
});
rangeVolume.addEventListener('mouseup', () => {
    volume.style.scale = '1';
    volume.style.height = '10px';
    volume.style.boxShadow = '';
    rangeVolume.blur();
});


function playOnClick() {
    if (!audio.paused){
        audio.pause();
        miniCover.style.cssText = 'width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97); transform: scale(0.94); filter: brightness(80%)';
        cover.style.cssText = 'animation: rotate 10s linear infinite; width: 400px; animation-play-state: paused; filter: brightness(80%) grayscale(40%);';
        playButton.innerHTML = '⏵';
    } else {
        audio.play();
        miniCover.style.cssText = 'width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97);';
        cover.style.cssText = 'animation: rotate 10s linear infinite; width: 400px; animation-play-state: running;';
        playButton.innerHTML = '⏸';
    }
    playButton.blur();
}


function changeTrack(pressedBtn) {
    let isPaused = true;

    if (pressedBtn == 'next') {
        currenttrack++;
    }
    else {
        currenttrack--;
    }

    if (!audio.paused){
        isPaused = false;
        playOnClick();
    }

    audio.setAttribute('src', ('./music/' + tracks[currenttrack]).toString());
    cover.setAttribute('src', ('./music/covers/' + covers[currenttrack]).toString());
    miniCover.setAttribute('src', ('./music/covers/' + covers[currenttrack]).toString());
    trackName.innerHTML = names[currenttrack].toUpperCase();
    playerTrackName.innerHTML = names[currenttrack].toUpperCase();

    if (!isPaused) {
        playOnClick();
    }
}


function workingProgressBar(){
    if (audio.paused == false){
        currentTime();
    }

    function currentTime(){
    progressBar.setAttribute('max', (audio.duration - 0.2).toString());
    progressBar.setAttribute('value', audio.currentTime.toString());
    }

    if ((audio.duration === audio.currentTime) && (!isInput)) {
        currenttrack++;

        playOnClick();

        audio.setAttribute('src', ('./music/' + tracks[currenttrack]).toString());
        cover.setAttribute('src', ('./music/covers/' + covers[currenttrack]).toString());
        miniCover.setAttribute('src', ('./music/covers/' + covers[currenttrack]).toString());
        trackName.innerHTML = names[currenttrack].toUpperCase();
        playerTrackName.innerHTML = names[currenttrack].toUpperCase();
        
        playOnClick();
    }
}
setInterval(workingProgressBar, 50);

function ff(){

    progressBar.setAttribute('value', '10');
}