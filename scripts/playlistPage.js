function collapseAll() {
	if (isOpened) {
		openPlayer();
	}

	main.style = "";

	liked.style =
		"margin-top: -1000px; filter: blur(30px); transform: scale(0.8)";

	document.querySelector(".logo").blur();
}

function openLiked() {
	if (isOpened) {
		openPlayer();
	}

	if (main.style.marginTop === "150vh") {
		main.style = "";
		liked.style =
			"margin-top: -1000px; filter: blur(30px); transform: scale(0.8)";
	} else {
		liked.style = "";
		main.style.marginTop = "150vh";
		main.style.filter = "blur(30px)";
		main.style.opacity = "0";
		main.style.transform = "scale(0.8)";
	}

	document.querySelector(".nav-liked").blur();
}
