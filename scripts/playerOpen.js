karaokeText.style.opacity = '0';
karaokeText.style.transform = 'scale(0.3)';

function openPlayer(){
    if (isOpened === false){
        footer.style.height = '100%';
        main.style.transform= 'scale(0.6)';
        main.style.filter = 'blur(20px)';
        karaokeText.style.opacity = '1';
        karaokeText.style.transform = 'scale(1)';
        isOpened = true;
    } else {
        karaokeText.style.opacity = '0';
        karaokeText.style.transform = 'scale(0.3)';
        footer.style.height = '85px';
        main.style.transform= 'scale(1)';
        main.style.filter = 'blur(0)';
        isOpened = false;
    }
}

let k = 0;

function audioText(){
    audio.addEventListener('playing', gg());
    function gg(){
        karaokeLi.style.marginTop = (-64 * parseInt(audio.currentTime * 0.65)).toString() + 'px';
    }
}
setInterval(audioText, 50);