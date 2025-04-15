//Проигрывание аудиофайла
function playOnClick() {
    if (!audio.paused){
        audio.pause();
        miniCover.style.cssText = 'width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97); transform: scale(0.94); filter: brightness(80%); cursor:pointer';
        cover.style.cssText = 'animation: rotate 10s linear infinite; width: 400px; animation-play-state: paused; filter: brightness(80%) grayscale(40%);';
        playerTrackName.style.letterSpacing = '2px';
        playButton.innerHTML = '&#9205';
    } else {
        audio.play();
        miniCover.style.cssText = 'width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97); cursor:pointer';
        cover.style.cssText = 'animation: rotate 10s linear infinite; width: 400px; animation-play-state: running;';
        playButton.innerHTML = '&#9208;';
        playerTrackName.style.letterSpacing = '5px';

        karaokeText.innerHTML = '';

        for (let i = parseInt(audio.currentTime); i < trackText.length; i++){
            let kg = document.createElement('li');
            kg.innerHTML = trackText[i];
            karaokeText.innerHTML += '<li id="karaokeLi">' + kg.innerHTML + '</li>';
        }
    }
    playButton.blur();
}


//Смена аудиофайла
function changeTrack(pressedBtn) {
    let isPaused = true;

    if (pressedBtn == 'next') {
        if ((currenttrack + 1) >= tracks.length){
            currenttrack = 0;
        } else {
            currenttrack++;
        }
    }
    else {
        if (audio.currentTime < 3){
            if (currenttrack - 1 < 0){
                audio.currentTime = 0;
            } else {
                currenttrack--;
            }
        } else {
            audio.currentTime = 0;
        }
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