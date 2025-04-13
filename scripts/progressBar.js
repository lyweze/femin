//Функция обновления прогрессбара
function workingProgressBar(){
    let minutes = false;
    let timeOfTrack = parseInt(audio.currentTime);

    if (timeOfTrack >= 60){
        minutes = true;

        if ((timeOfTrack - 60 * parseInt(timeOfTrack/60)) <= 9){
            timeOfTrack = parseInt(timeOfTrack/60).toString() + ':0' + (timeOfTrack - 60 * parseInt(timeOfTrack/60)).toString();
        } else {
            timeOfTrack = parseInt(timeOfTrack/60).toString() + ':' + (timeOfTrack - 60 * parseInt(timeOfTrack/60)).toString();
        }
    }

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

    if (minutes === false){
        if (timeOfTrack <= 9){
            trackTime.innerHTML = '0:0' + timeOfTrack.toString();
        } else {
            trackTime.innerHTML = '0:' + timeOfTrack.toString();
        }
    } else {
        trackTime.innerHTML = timeOfTrack.toString();
    }
}

//Обновляю прогрессбар
setInterval(workingProgressBar, 50);