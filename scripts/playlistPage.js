window.addEventListener("wheel", (event) => {
	const delta = event.deltaY;

	let lk;
	let pl;

	if (main.style.marginTop === "130vh") {
		lk = true;
	}
	if (main.style.marginTop === "-80vh") {
		pl = true;
	}

	if (delta > 0) {
		main.style = "margin-top: -80vh; filter: blur(30px); transform: scale(0.8)";
		playlists.style = "";
        liked.style =
		"margin-top: -1000px; filter: blur(30px); transform: scale(0.8)";
	} else {
		main.style = "margin-top: 130vh; filter: blur(30px); transform: scale(0.8)";
		liked.style = "";
        playlists.style =
		"margin-top: 1000px; filter: blur(30px); transform: scale(0.8)";
	}
});

function collapseAll() {
	main.style = "";

	playlists.style =
		"margin-top: 1000px; filter: blur(30px); transform: scale(0.8)";

	liked.style =
		"margin-top: -1000px; filter: blur(30px); transform: scale(0.8)";
}

function openPlaylists() {
	liked.style =
		"margin-top: -1000px; filter: blur(30px); transform: scale(0.8)";

	if (main.style.marginTop === "-80vh") {
		main.style = "";
		playlists.style =
			"margin-top: 1000px; filter: blur(30px); transform: scale(0.8)";
	} else {
		main.style.marginTop = "-80vh";
		main.style.filter = "blur(30px)";
		main.style.transform = "scale(0.8)";
		playlists.style = "";
	}
}

function openLiked() {
	playlists.style = "";

	if (main.style.marginTop === "130vh") {
		main.style = "";
		playlists.style =
			"margin-top: 1000px; filter: blur(30px); transform: scale(0.8)";
		liked.style =
			"margin-top: -1000px; filter: blur(30px); transform: scale(0.8)";
	} else {
		liked.style = "";
		main.style.marginTop = "130vh";
		main.style.filter = "blur(30px)";
		main.style.transform = "scale(0.8)";
		playlists.style =
			"margin-top: 1000px; filter: blur(30px); transform: scale(0.8)";
	}
}

function moveToLike(){
	console.log('liked ' + currenttrack);
}