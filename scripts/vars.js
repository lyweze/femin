//Переменные
let audio = document.getElementById("audioPlayer"); //Аудиофайл
let trackName = document.getElementById("trackName"); //Имя трека
let playerTrackName = document.getElementById("playerTrackName"); //Имя трека (на футере плеера)
let cover = document.getElementById("cover"); //Обложка
let miniCover = document.getElementById("mini-cover"); //Мини-обложка
let playButton = document.getElementById("playButton"); //Кнопка проигрывания || паузы
let nextButton = document.querySelector(".nextButton"); //Следующий трек
let previousButton = document.querySelector(".previousButton"); //Предыдущий трек
let progressBar = document.getElementById("progressBar"); //Прогрессбар
let rangeProgress = document.getElementById("rangeProgress"); //Изменение прогресса
let trackTime = document.getElementById("trackTime"); //Время трека на прогрессбаре
let volume = document.getElementById("volume"); //Звук
let rangeVolume = document.getElementById("rangeVolume"); //Изменение громкости
let currenttrack = 0; //Текущий трек
let footer = document.getElementById("footer"); //Весь футер
let main = document.getElementById("main"); //Main блок
let playList = document.getElementById("playList"); //Текущий плейлист
let playlists = document.getElementById("article1"); //Плейлисты
let liked = document.getElementById("article2"); //Плейлисты избранное
let addToLike = document.getElementById("addToLike");
let playlist = document.getElementById("playlist"); //Плейлисты (блоки)
let likedPlayList = document.getElementById("likedPlayList"); //Плейлист избранное
let playlistElement = document.getElementById("playlistElement");
let jsonParsed;

let pageWidth = document.documentElement.scrollWidth;
let isOpened = false;
let isInput = false;

class currentTrack {
	constructor(json) {
		this.track_id = json.track_id;
		this.title = json.title;
		this.mp3_url = json.mp3_url;
		this.cover_url = json.cover_url;
	}
}

let likedTracks = [];
let cachedTracks = [];

fetch("https://femin.onrender.com/tracks")
	.then((response) => {
		return response.json();
	})

	.then((json) => {
		jsonParsed = json;
	})

	.catch((error) => console.error("Ошибка при исполнении запроса: ", error));
