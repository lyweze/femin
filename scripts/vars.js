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
let liked = document.getElementById("article2"); //Плейлисты
let playlist = document.getElementById("playlist"); //Плейлисты (блоки)
let likedPlayList = document.getElementById("likedPlayList"); //Плейлист избранное
let pageWidth = document.documentElement.scrollWidth;
let isOpened = false;
let isInput = false;

const tracks = ["moskva.mp3", "casino.mp3", "magnolia.mp3", "zloy_zhora.mp3"];

const covers = [
	"moskva.jpeg",
	"casino.jpeg",
	"magnolia.jpeg",
	"zloy_zhora.jpeg",
];

const names = ["москва", "casino", "magnolia", "злой жора"];

const likedTracks = [];
