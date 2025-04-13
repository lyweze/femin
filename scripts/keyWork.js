//Управление клавивтурой
window.addEventListener('keydown', (event) => {
    nextButton.blur();
    previousButton.blur();
    
    switch (event.keyCode){
        case 39: audio.currentTime += 5; progressBar.setAttribute('value', audio.currentTime.toString()); break;
        case 37: audio.currentTime -= 5; progressBar.setAttribute('value', audio.currentTime.toString()); break;
        case 32: playOnClick(); break;
        case 38: if ((audio.volume + 0.1) > 1){audio.volume = 1;}else{audio.volume += 0.1;}; volume.setAttribute('value', audio.volume.toString()); break;
        case 40: audio.volume -= 0.1; volume.setAttribute('value', audio.volume.toString()); break;
    }
});