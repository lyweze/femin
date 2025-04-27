//Функция обновления прогрессбара
function workingProgressBar() {
	if (jsonParsed != null) {
		if (jsonParsed[currenttrack].track_id === 40 && audio.currentTime >= 14.7) {
			main.style.backgroundImage =
				"https://i.pinimg.com/736x/73/d9/3b/73d93b467894822c127d6f6a2d785ee5.jpg";
			cover.setAttribute(
				"src",
				"https://i.pinimg.com/736x/73/d9/3b/73d93b467894822c127d6f6a2d785ee5.jpg"
			);
			miniCover.setAttribute(
				"src",
				"https://i.pinimg.com/736x/73/d9/3b/73d93b467894822c127d6f6a2d785ee5.jpg"
			);
			trackName.innerHTML = "☠️💀💀💀☠️☠️☠️☠️☠️💀💀💀💀";
			playerTrackName.innerHTML = "☠️💀💀💀☠️☠️☠️☠️☠️💀💀💀💀";
			document.querySelector(".logo").innerHTML = "💀💀💀💀💀";
		} else {
			document.querySelector(".logo").innerHTML = "femin";
		}
	}

	let minutes = false;
	let timeOfTrack = parseInt(audio.currentTime);

	// Проверяю время (>= 60с => перевожу в минуты)
	if (timeOfTrack >= 60) {
		minutes = true;

		if (timeOfTrack - 60 * parseInt(timeOfTrack / 60) <= 9) {
			timeOfTrack =
				parseInt(timeOfTrack / 60).toString() +
				":0" +
				(timeOfTrack - 60 * parseInt(timeOfTrack / 60)).toString();
		} else {
			timeOfTrack =
				parseInt(timeOfTrack / 60).toString() +
				":" +
				(timeOfTrack - 60 * parseInt(timeOfTrack / 60)).toString();
		}
	}

	// Настройка диапазона прогрессбара
	if (audio.paused == false) {
		currentTime();
	}
	function currentTime() {
		progressBar.setAttribute("max", (audio.duration - 0.2).toString());
		progressBar.setAttribute("value", audio.currentTime.toString());
	}

	// Переключение трека по завершению
	if (audio.duration === audio.currentTime && !isInput) {
		audio.volume = 0;
		playOnClick();

		function moveTrackIfEnded(json) {
			let isPaused = true;

			if (!audio.paused) {
				isPaused = false;
				playOnClick();
			}

			if (currenttrack + 1 >= json.length) {
				currenttrack = 0;
			} else {
				currenttrack++;
			}

			let track = new currentTrack(json[currenttrack]);
			let currenttrack_exists = saveTrack(json, track, currenttrack);

			if (currenttrack_exists === true) {
				let currenttrack_id = 0;

				for (let i = 0; i < cachedTracks.length; i++) {
					if (track.track_id === cachedTracks[i].track_id) {
						currenttrack_id = i;
					}
				}

				cover.setAttribute("src", cachedTracks[currenttrack_id].cover_url);
				audio.setAttribute("src", cachedTracks[currenttrack_id].mp3_url);
				miniCover.setAttribute("src", cachedTracks[currenttrack_id].cover_url);
				trackName.innerHTML = cachedTracks[currenttrack_id].title;
				playerTrackName.innerHTML = cachedTracks[currenttrack_id].title;
			} else {
				cover.setAttribute("src", track.cover_url);
				audio.setAttribute("src", track.mp3_url);
				miniCover.setAttribute("src", track.cover_url);
				trackName.innerHTML = track.title;
				playerTrackName.innerHTML = track.title;
			}

			audio.volume = 1;

			if (!isPaused) {
				playOnClick();
			}

			if (minutes === false) {
				if (timeOfTrack <= 9) {
					trackTime.innerHTML = "0:0" + timeOfTrack.toString();
				} else {
					trackTime.innerHTML = "0:" + timeOfTrack.toString();
				}
			} else {
				trackTime.innerHTML = timeOfTrack.toString();
			}

			if (!likedTracks.includes(track.track_id)) {
				addToLike.innerHTML =
					'<svg xmlns="http://www.w3.org/2000/svg"width="32"height="32"fill="currentColor"class="bi bi-heart" viewBox="0 0 16 16"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/></svg>';
			} else {
				addToLike.innerHTML =
					'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>';
			}
		}

		if (jsonParsed === null) {
			fetch("https://femin.onrender.com/tracks")
				.then((response) => {
					return response.json();
				})

				.then((json) => {
					moveTrackIfEnded(json);
				});
		} else {
			moveTrackIfEnded(jsonParsed);
		}
	}

	// Навожу красоту
	if (minutes === false) {
		if (timeOfTrack <= 9) {
			trackTime.innerHTML = "0:0" + timeOfTrack.toString();
		} else {
			trackTime.innerHTML = "0:" + timeOfTrack.toString();
		}
	} else {
		trackTime.innerHTML = timeOfTrack.toString();
	}
}

//Обновляю прогрессбар
setInterval(workingProgressBar, 50);

//Перелистывание прогрессбара
rangeProgress.addEventListener("input", () => {
	isInput = true;

	if (!audio.paused) {
		audio.pause();
		cover.style.cssText =
			"animation: rotate 10s linear infinite; animation-play-state: paused;";
	}

	audio.currentTime = (audio.duration - 0.2) * (rangeProgress.value / 100);
	progressBar.setAttribute("max", audio.duration.toString());
	progressBar.setAttribute("value", audio.currentTime.toString());
	progressBar.style.scale = "1.03";
	progressBar.style.boxShadow = "0 0 10px rgba(128, 52, 163, 0.35)";
});
rangeProgress.addEventListener("mouseup", () => {
	isInput = false;

	if (cover.style.filter != "brightness(80%) grayscale(40%)") {
		audio.play();
		cover.style.cssText =
			"animation: rotate 10s linear infinite; animation-play-state: running;";
	}

	progressBar.style.scale = "1";
	progressBar.style.boxShadow = "";
	rangeProgress.blur();
});

//Изменение громоксти
rangeVolume.addEventListener("input", () => {
	audio.volume = rangeVolume.value;
	volume.setAttribute("value", audio.volume.toString());
	volume.style.scale = "1.01";
	volume.style.height = "30px";
	volume.style.boxShadow = "0 0 20px rgba(128, 52, 163, 0.35)";
	volume.style.borderRadius = "6px";
});
rangeVolume.addEventListener("mouseup", () => {
	volume.style.scale = "1";
	volume.style.height = "10px";
	volume.style.boxShadow = "";
	volume.style.borderRadius = "0px";
	rangeVolume.blur();
});
