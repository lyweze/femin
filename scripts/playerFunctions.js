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
		playerTrackName.style.letterSpacing = "3px";
	}

	playlistElement.innerText = '#playList {li:nth-child(' + parseInt(currenttrack + 1) + '){background-color: #ffffff52;}}';

	playButton.blur();
}

//Смена аудиофайла
function settrack(key, n) {
	fetch("https://femin.onrender.com/tracks")
		.then((response) => {
			return response.json();
		})

		.then((json) => {
			let isPaused = true;

			if (!audio.paused) {
				isPaused = false;
				playOnClick();
			}

			if (key === "next") {
				if (currenttrack + 1 >= json.length) {
					currenttrack = 0;
				} else {
					currenttrack++;
				}
			} else if (key === "previous") {
				if (audio.currentTime < 3) {
					if (currenttrack - 1 < 0) {
						currenttrack = json.length - 1;
					} else {
						currenttrack--;
					}
				} else {
					audio.currentTime = 0;
				}
			}

			if (n != undefined) {
				currenttrack = +n;
			}

			let track = new currentTrack(json[currenttrack]);

			cover.setAttribute("src", track.cover_url);
			audio.setAttribute("src", track.mp3_url);
			miniCover.setAttribute("src", track.cover_url);
			trackName.innerHTML = track.title;
			playerTrackName.innerHTML = track.title;

			if (!isPaused) {
				playOnClick();
			}
		})

		.catch((error) => console.error("Ошибка при исполнении запроса: ", error));
}
settrack();

function goToTrack(name) {
	currenttrack = +name;

	settrack("", currenttrack);
	playlistElement.innerText = '#playList {li:nth-child(' + parseInt(currenttrack + 1) + '){background-color: #ffffff52;}}';
}