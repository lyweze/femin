//Переменные
/* ------------------------------------------------------------ */
/* STARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTART */
//Переменные для функционала
const audio = document.getElementById("audioPlayer"); //Аудиофайл
let currenttrack = 0; //Текущий трек
const playlistElement = document.getElementById("playlistElement"); //inline стиль (использую для выделения трека в текущем плейлисте)
let isOpened = false; //Проверка открыт ли плейлист
let jsonParsed; //JSON полученный с сервака (созраняю, чтоб вечно не отправлять запросы в бд при обычном использовании)
let likedTracks = []; //Лайкнутые
let cachedTracks = []; //Кэшируемые треки
let isInput = false;

//Класс для текущего трека
class currentTrack {
	constructor(json) {
		this.track_id = json.track_id;
		this.title = json.title;
		this.mp3_url = json.mp3_url;
		this.cover_url = json.cover_url;
	}
}

//Запращиваю JSON с сервака и переножу ответ в переменную jsonParsed
fetch("https://femin.onrender.com/tracks")
	.then((response) => {
		return response.json();
	})
	.then((json) => {
		jsonParsed = json;
	})
	.catch((error) => console.error("Ошибка при исполнении запроса: ", error));

/* ------------------------------------------------------------ */
/* ENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDEND */
//
//
//
//
//
/* ------------------------------------------------------------ */
/* STARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTART */
//Основной блок
const main = document.getElementById("main"); //Main блок
const trackName = document.getElementById("trackName"); //Имя трека
const cover = document.getElementById("cover"); //Обложка

//?????? mb pomenyat
let addToLike = document.getElementById("addToLike"); //Кнопка добавить в избранное/удалить из избранного
/* ------------------------------------------------------------ */
/* ENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDEND */
//
//
//
//
//
/* ------------------------------------------------------------ */
/* STARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTART */
//Футер (проигрыватель)
const footer = document.getElementById("footer"); //Весь футер
const playerTrackName = document.getElementById("playerTrackName"); //Имя трека (на футере плеера)
const miniCover = document.getElementById("mini-cover"); //Мини-обложка
const playButton = document.getElementById("playButton"); //Кнопка проигрывания || паузы
const nextButton = document.querySelector(".nextButton"); //Следующий трек
const previousButton = document.querySelector(".previousButton"); //Предыдущий трек
const progressBar = document.getElementById("progressBar"); //Прогрессбар
const rangeProgress = document.getElementById("rangeProgress"); //Изменение прогресса
const trackTime = document.getElementById("trackTime"); //Время трека на прогрессбаре
const volume = document.getElementById("volume"); //Звук
const rangeVolume = document.getElementById("rangeVolume"); //Изменение громкости

//Текущий плейлист
const playList = document.getElementById("playList"); //Текущий плейлист
/* ------------------------------------------------------------ */
/* ENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDEND */
//
//
//
//
//
/* ------------------------------------------------------------ */
/* STARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTARTSTART */
//Несортированное
const liked = document.getElementById("likedSection"); //Плейлисты избранное
const likedSectionText = document.getElementById("likedSectionText"); //Текст в блоке избранного
const likedPlayList = document.getElementById("likedPlayList"); //Плейлист избранное
/* ------------------------------------------------------------ */
/* ENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDENDEND */
