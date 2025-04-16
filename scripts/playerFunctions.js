//Проигрывание аудиофайла
function playOnClick() {
	if (!audio.paused) {
		audio.pause();
		miniCover.style.cssText =
			"width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97); transform: scale(0.94); filter: brightness(80%); cursor:pointer";
		cover.style.cssText =
			"animation: rotate 10s linear infinite; animation-play-state: paused; filter: brightness(80%) grayscale(40%);";
		playerTrackName.style.letterSpacing = "2px";
		playButton.innerHTML =
			'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-play-fill" viewBox="0 0 15 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/></svg>';
	} else {
		audio.play();
		miniCover.style.cssText =
			"width: 65px; border-radius: 8px; margin-left: 10px; transition: all 0.3s cubic-bezier(.45,.06,.19,.97); cursor:pointer";
		cover.style.cssText =
			"animation: rotate 10s linear infinite; animation-play-state: running;";
		playButton.innerHTML =
			'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-pause-fill" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/></svg>';
		playerTrackName.style.letterSpacing = "5px";
	}

	playList.innerHTML = "";
	for (let i = 0; i < tracks.length; i++) {
		if (i == currenttrack) {
			playList.innerHTML +=
				'<li style="background-color: #ffffff52" onclick="goToTrack(' +
				"'" +
				i +
				"')" +
				'"' +
				'><img src="./music/covers/' +
				covers[i] +
				'"</img><p>' +
				names[i] +
				"</p></li>";
		} else {
			playList.innerHTML +=
				'<li onclick="goToTrack(' +
				"'" +
				i +
				"')" +
				'"' +
				'><img src="./music/covers/' +
				covers[i] +
				'"</img><p>' +
				names[i] +
				"</p></li>";
		}
	}

	playButton.blur();
}

//Смена аудиофайла
function changeTrack(pressedBtn) {
	let isPaused = true;

	if (pressedBtn == "next") {
		if (currenttrack + 1 >= tracks.length) {
			currenttrack = 0;
		} else {
			currenttrack++;
		}
	} else {
		if (audio.currentTime < 3) {
			if (currenttrack - 1 < 0) {
				currenttrack = tracks.length - 1;
			} else {
				currenttrack--;
			}
		} else {
			audio.currentTime = 0;
		}
	}

	if (!audio.paused) {
		isPaused = false;
		playOnClick();
	}

	audio.setAttribute("src", ("./music/" + tracks[currenttrack]).toString());
	cover.setAttribute(
		"src",
		("./music/covers/" + covers[currenttrack]).toString()
	);
	miniCover.setAttribute(
		"src",
		("./music/covers/" + covers[currenttrack]).toString()
	);
	trackName.innerHTML = names[currenttrack].toUpperCase();
	playerTrackName.innerHTML = names[currenttrack].toUpperCase();

	if (!isPaused) {
		playOnClick();
	}
}

function goToTrack(name) {
	currenttrack = +name + 1;

	changeTrack();
}
