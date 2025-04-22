playList.style.opacity = "0";

playList.innerHTML = "";
fetch("./music/tracks.json")
	.then((response) => {
		return response.json();
	})

	.then((json) => {
		for (let i = 0; i < json.length; i++) {
			if (i == currenttrack) {
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
			} else {
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
		}

		playlistElement.innerText =
			"#playList {li:nth-child(" +
			parseInt(currenttrack + 1) +
			"){background-color: #ffffff52;}}";
	})

	.catch((error) => console.error("Ошибка при исполнении запроса: ", error));

function openPlayer() {
	let lk;
	let pl;

	if (main.style.marginTop === "130vh") {
		lk = true;
	}
	if (main.style.marginTop === "-80vh") {
		pl = true;
	}

	if (isOpened === false) {
		footer.style.height = "80%";
		playList.style.opacity = "1";
		playList.style.transform = "scale(1)";
		playList.style.filter = "";
		playList.style.height = "calc(100% - 85px)";

		main.style.transform = "scale(0.6)";
		main.style.filter = "blur(20px)";

		if (lk === true) {
			liked.style.transform = "scale(0.6)";
			liked.style.filter = "blur(20px)";
		}
		if (pl === true) {
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
		}
		if (pl === true) {
			playlists.style.transform = "";
			playlists.style.filter = "";
		} else {
			main.style.transform = "";
			main.style.filter = "";
		}

		isOpened = false;
	}
}
