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

	playlistElement.innerText =
		"#playList {li:nth-child(" +
		parseInt(currenttrack + 1) +
		"){background-color: #ffffff52;}}" +
		"#likedPlayList {li:nth-child(" +
		parseInt(currenttrack + 1) +
		"){background-color: #ffffff52;}}";

	playButton.blur();
}

//Смена аудиофайла
function settrack(key, n) {
	function moveTrack(json) {
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

		if (!likedTracks.includes(currenttrack)) {
			addToLike.innerHTML =
				'<svg xmlns="http://www.w3.org/2000/svg"width="32"height="32"fill="currentColor"class="bi bi-heart" viewBox="0 0 16 16"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/></svg>';
		} else {
			addToLike.innerHTML =
				'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>';
		}

		if (!isPaused) {
			playOnClick();
		}
	}

	if (key === "previous" && audio.currentTime > 3) {
		audio.currentTime = 0;
	} else {
		if (jsonParsed != null) {
			moveTrack(jsonParsed);
		} else {
			fetch("https://femin.onrender.com/tracks")
				.then((response) => {
					return response.json();
				})

				.then((json) => {
					moveTrack(json);
				});
		}
	}
}
settrack();

//Сохраняю прослушанный или пролистанный трек
function saveTrack(json_, track, i) {
	let isExists = false;

	if (cachedTracks.length > 0) {
		for (let j = 0; j < cachedTracks.length; j++) {
			if (cachedTracks[j].track_id == track.track_id) {
				isExists = true;
			}
		}
	}

	if (!isExists) {
		fetch(json_[i].mp3_url)
			.then((response) => {
				return response.blob();
			})
			.then((blob) => {
				track.mp3_url = URL.createObjectURL(blob);
			});

		fetch(json_[i].cover_url)
			.then((response) => {
				return response.blob();
			})
			.then((blob) => {
				track.cover_url = URL.createObjectURL(blob);

				cachedTracks.push(track);
			});
	}

	return isExists;
}

//Смена трека по нажатию в текущем плйлисте
function goToTrack(name) {
	currenttrack = +name;

	settrack("", currenttrack);
	playlistElement.innerText =
		"#playList {li:nth-child(" +
		parseInt(currenttrack + 1) +
		"){background-color: #ffffff52;}}" +
		"#likedPlayList {li:nth-child(" +
		parseInt(currenttrack + 1) +
		"){background-color: #ffffff52;}}";
}

//Добавить в избранное
function moveToLike() {
	if (!likedTracks.includes(jsonParsed[currenttrack].track_id)) {
		likedTracks.push(jsonParsed[currenttrack].track_id);

		addToLike.innerHTML =
			'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>';
	} else {
		for (let i = 0; i < likedTracks.length; i++) {
			if (likedTracks[i] === jsonParsed[currenttrack].track_id) {
				likedTracks.splice(i, 1);
			}
		}

		addToLike.innerHTML =
			'<svg xmlns="http://www.w3.org/2000/svg"width="32"height="32"fill="currentColor"class="bi bi-heart" viewBox="0 0 16 16"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/></svg>';
	}
	addToLike.blur();

	function createLikedPlaylist(json) {
		likedPlayList.innerHTML = "";
		for (let i = 0; i < json.length; i++) {
			if (likedTracks.includes(json[i].track_id)) {
				likedPlayList.innerHTML +=
					'<li onclick="goToTrack(' +
					"'" +
					i +
					"')" +
					'"' +
					'><img src="' +
					json[i].cover_url +
					'"</img><p>' +
					json[i].title +
					"</p></li>";
			}
		}

		playlistElement.innerText =
			"#playList {li:nth-child(" +
			parseInt(currenttrack + 1) +
			"){background-color: #ffffff52;}}" +
			"#likedPlayList {li:nth-child(" +
			parseInt(currenttrack + 1) +
			"){background-color: #ffffff52;}}";
	}

	createLikedPlaylist(jsonParsed);
}
