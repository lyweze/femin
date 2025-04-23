//Управление клавивтурой
window.addEventListener("keydown", (event) => {
	nextButton.blur();
	previousButton.blur();

	switch (event.keyCode) {
		case 39:
			isInput = true;
			if (audio.currentTime + 5 > audio.duration) {
				audio.currentTime = audio.duration;
			} else {
				audio.currentTime += 5;
			}
			progressBar.setAttribute("value", audio.currentTime.toString());
			break;
		case 37:
			isInput = true;
			audio.currentTime -= 5;
			progressBar.setAttribute("value", audio.currentTime.toString());
			break;
		case 32:
			playOnClick();
			break;
		case 38:
			if (audio.volume + 0.1 <= 1) {
				audio.volume += 0.1;
			}
			volume.setAttribute("value", audio.volume.toString());
			break;
		case 40:
			if (audio.volume - 0.1 >= 0) {
				audio.volume -= 0.1;
			}
			volume.setAttribute("value", audio.volume.toString());
			break;
	}
});
window.addEventListener("keyup", () => {
	isInput = false;
});
