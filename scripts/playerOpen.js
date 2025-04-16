karaokeText.style.opacity = "0";
karaokeText.style.transform = "scale(0.3)";

function openPlayer() {
	if (isOpened === false) {
		footer.style.height = "80%";
		main.style.transform = "scale(0.6)";
		main.style.filter = "blur(20px)";
		karaokeText.style.opacity = "1";
		karaokeText.style.transform = "scale(1)";
		karaokeText.style.filter = "";
		karaokeText.style.height = "50%";
		isOpened = true;
	} else {
		karaokeText.style.opacity = "0";
		karaokeText.style.transform = "scale(0.3)";
		karaokeText.style.filter = "blur(3px)";
		footer.style.height = "85px";
		main.style.transform = "scale(1)";
		main.style.filter = "blur(0)";
		karaokeText.style.height = "0";
		isOpened = false;
	}
}