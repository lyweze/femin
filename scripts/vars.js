//Переменные
let audio = document.getElementById('audioPlayer'); //Аудиофайл
let trackName = document.getElementById('trackName'); //Имя трека
let playerTrackName = document.getElementById('playerTrackName'); //Имя трека (на футере плеера)
let cover = document.getElementById('cover'); //Обложка
let miniCover = document.getElementById('mini-cover'); //Мини-обложка
let playButton = document.getElementById('playButton'); //Кнопка проигрывания || паузы
let nextButton = document.querySelector('.nextButton'); //Следующий трек
let previousButton = document.querySelector('.previousButton'); //Предыдущий трек
let progressBar = document.getElementById('progressBar'); //Прогрессбар
let rangeProgress = document.getElementById('rangeProgress'); //Изменение прогресса
let trackTime = document.getElementById('trackTime'); //Время трека на прогрессбаре
let volume = document.getElementById('volume'); //Звук
let rangeVolume = document.getElementById('rangeVolume'); //Изменение громкости
let currenttrack = 0; //Текущий трек
let footer = document.getElementById('footer'); //Весь футер
// let footerDiv = document.getElementById('footer-div'); //Блок с элементами
let main = document.getElementById('main'); //Main блок
let karaokeText = document.getElementById('karaokeText'); //Текст песни (список)
// let karaokeLi = document.getElementById('karaokeLi'); //Строчка текста песни
let isOpened = false;

let ad = 'Еду сейчас на Москва-Сити; Долбоёбы, хуй сосите; Я только прилетел с Ростова,; завтра улетаю в Питер; Сисястых сук ебать их давно; профи — не любитель;Я сам себе предприниматель,; вижу лохов — наебать их;Чёрная рубашка, галстук;— я уже мужчина;Её туфли зацепили,; ведь они из крокодила;Первый день в Москве,; мы закрываем всю дрочильню;Я сейчас на чилле, так что,; шлюха, подрочи мне;'

let trackText = ad.split(';');


//??
const tracks = ['moskva.mp3', 'casino.mp3','magnolia.mp3'];


const covers = ['moskva.jpeg', 'casino.jpeg', 'magnolia.jpeg'];
const names = ['москва', 'casino','magnolia'];