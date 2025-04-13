//Проигрывание аудиофайла
function playOnClick() {
    if (!audio.paused){
        audio.pause();
        miniCover.style.cssText = 'width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97); transform: scale(0.94); filter: brightness(80%)';
        cover.style.cssText = 'animation: rotate 10s linear infinite; width: 400px; animation-play-state: paused; filter: brightness(80%) grayscale(40%);';
        playerTrackName.style.letterSpacing = '10%';
        playButton.innerHTML = '⏵';
    } else {
        audio.play();
        miniCover.style.cssText = 'width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97);';
        cover.style.cssText = 'animation: rotate 10s linear infinite; width: 400px; animation-play-state: running;';
        playButton.innerHTML = '⏸';
        playerTrackName.style.letterSpacing = '20%';
    }
    playButton.blur();
}


//Смена аудиофайла
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