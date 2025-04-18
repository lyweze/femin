playList.style.opacity = "0";
// playList.style.transform = "scale(0.3)";

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
		// playList.style.transform = "scale(0.1)";
		playList.style.filter = "blur(30px)";
		// playList.style.height = "0";
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
