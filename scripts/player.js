//Перелистывание времени аудиофайла
rangeProgress.addEventListener("input", () => {
	isInput = true;
	audio.pause();
	cover.style.cssText =
		"animation: rotate 10s linear infinite; animation-play-state: paused;";
	audio.currentTime = (audio.duration - 0.2) * (rangeProgress.value / 100);
	progressBar.setAttribute("max", audio.duration.toString());
	progressBar.setAttribute("value", audio.currentTime.toString());
	progressBar.style.scale = "1.03";
	progressBar.style.boxShadow = "0 0 10px rgba(128, 52, 163, 0.35)";
});
rangeProgress.addEventListener("mouseup", () => {
	isInput = false;
	audio.play();
	cover.style.cssText =
		"animation: rotate 10s linear infinite; animation-play-state: running;";
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
