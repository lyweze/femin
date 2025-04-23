function collapseAll() {
	if (isOpened) {
		openPlayer();
	}

	main.style = "";

	playlists.style =
		"margin-top: 1000px; filter: blur(30px); transform: scale(0.8)";

	liked.style =
		"margin-top: -1000px; filter: blur(30px); transform: scale(0.8)";
}

function openPlaylists() {
	if (isOpened) {
		openPlayer();
	}

	liked.style =
		"margin-top: -1000px; filter: blur(30px); transform: scale(0.8)";

	if (main.style.marginTop === "-100vh") {
		main.style = "";
		playlists.style =
			"margin-top: 1000px; filter: blur(30px); transform: scale(0.8)";
	} else {
		main.style.marginTop = "-100vh";
		main.style.filter = "blur(30px)";
		main.style.opacity = "0";
		main.style.transform = "scale(0.8)";
		playlists.style = "";
	}
}

function openLiked() {
	if (isOpened) {
		openPlayer();
	}

	playlists.style = "";

	if (main.style.marginTop === "150vh") {
		main.style = "";
		playlists.style =
			"margin-top: 1000px; filter: blur(30px); transform: scale(0.8)";
		liked.style =
			"margin-top: -1000px; filter: blur(30px); transform: scale(0.8)";
	} else {
		liked.style = "";
		main.style.marginTop = "150vh";
		main.style.filter = "blur(30px)";
		main.style.opacity = "0";
		main.style.transform = "scale(0.8)";
		playlists.style =
			"margin-top: 1000px; filter: blur(30px); transform: scale(0.8)";
	}
}
