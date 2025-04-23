//Функция обновления прогрессбара
function workingProgressBar() {
	let minutes = false;
	let timeOfTrack = parseInt(audio.currentTime);

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

	if (audio.paused == false) {
		currentTime();
	}

	function currentTime() {
		progressBar.setAttribute("max", (audio.duration - 0.2).toString());
		progressBar.setAttribute("value", audio.currentTime.toString());
	}

	if (audio.duration === audio.currentTime && !isInput) {
		audio.volume = 0;
		playOnClick();

		if (jsonParsed === null) {
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
						miniCover.setAttribute(
							"src",
							cachedTracks[currenttrack_id].cover_url
						);
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
				});
		} else {
			let isPaused = true;

			if (!audio.paused) {
				isPaused = false;
				playOnClick();
			}

			if (currenttrack + 1 >= jsonParsed.length) {
				currenttrack = 0;
			} else {
				currenttrack++;
			}

			let track = new currentTrack(jsonParsed[currenttrack]);
			let currenttrack_exists = saveTrack(jsonParsed, track, currenttrack);

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
		}
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
}

//Обновляю прогрессбар
setInterval(workingProgressBar, 50);
