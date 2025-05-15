// Отрисовываю текущий плейлист
playList.innerHTML = "";
function createCurrentPlaylist(json) {
	for (let i = 0; i < json.length; i++) {
		playList.innerHTML +=
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

	let currenttrackLIKED;
	for (let i = 0; i < likedTracks.length; i++) {
		if (likedTracks[i] === json[currenttrack].track_id) {
			currenttrackLIKED = i;
		}
	}

	playlistElement.innerText =
		"#playList {li:nth-child(" +
		parseInt(currenttrack + 1) +
		"){background-color: #ffffff52;}}" +
		"#likedPlayList {li:nth-child(" +
		parseInt(currenttrackLIKED + 1) +
		"){background-color: #ffffff52;}}";
}
if (jsonParsed != null) {
	createCurrentPlaylist(jsonParsed);
} else {
	fetch("https://femin.onrender.com/tracks")
		.then((response) => {
			return response.json();
		})

		.then((json) => {
			createCurrentPlaylist(json);
		})

		.catch((error) => console.error("Ошибка при исполнении запроса: ", error));
}

// Раскрытие плеера
function openPlayer() {
	let lk;
	let pl;

	if (main.style.marginTop === "150vh") {
		lk = true;
	}
	if (main.style.marginTop === "-100vh") {
		pl = true;
	}

	if (isOpened === false) {
		footer.style.height = "80%";
		playList.style.opacity = "1";
		playList.style.transform = "scale(1)";
		playList.style.filter = "";
		playList.style.height = "calc(100% - 105px)";

		if (lk === true) {
			liked.style.transform = "scale(0.6)";
			liked.style.filter = "blur(20px)";
		} else if (pl === true) {
			playlists.style.transform = "scale(0.6)";
			playlists.style.filter = "blur(20px)";
		} else {
			main.style.transform = "scale(0.6)";
			main.style.filter = "blur(20px)";
		}

		isOpened = true;
	} else {
		playList.style.opacity = "0";
		playList.style.filter = "blur(30px)";
		footer.style.height = "85px";

		if (lk === true) {
			liked.style.transform = "";
			liked.style.filter = "";
		} else if (pl === true) {
			playlists.style.transform = "";
			playlists.style.filter = "";
		} else {
			main.style.transform = "";
			main.style.filter = "";
		}

		isOpened = false;
	}
}
