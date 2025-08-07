
---
# Femin

[![GitHub](https://img.shields.io/github/license/lyweze/femin)](https://github.com/lyweze/femin)
[![GitHub last commit](https://img.shields.io/github/last-commit/lyweze/femin)](https://github.com/lyweze/femin/commits/main)
[![GitHub stars](https://img.shields.io/github/stars/lyweze/femin?style=social)](https://github.com/lyweze/femin)

Современный web-сервис для прослушивания музыки, работающий на открытом API.

- **Репозиторий:** [lyweze/femin](https://github.com/lyweze/femin)
- **Фронтенд:** [femin-front.netlify.app](https://femin-front.netlify.app/)
- **Апи** [femin.onrender.com](https://femin.onrender.com/)
## Возможности

- 🎵 Прослушивание музыки онлайн
- 🔍 Поиск треков и плейлистов
- 📂 Работа с плейлистами
- 🚀 Открытый API для интеграций
- 🐍 Backend на Python (FastAPI)
- ☁️ Интеграция с SoundCloud и Яндекс.Музыкой
- 🐳 Docker поддержка
  
## Превью
![](https://github.com/user-attachments/assets/ad3cc5af-f50f-4f8c-973b-2f67f8cb3020)


## Быстрый старт

### Требования
- Python 3.8+
- pip
- Docker (опционально)

### Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/lyweze/femin.git
   cd femin
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```
4. (Опционально) Запуск через Docker:
   ```bash
   docker build -t femin .
   docker run -p 8000:8000 femin
   ```

## Структура проекта

```
femin/
  app/
    main.py
    api/
      routes/
        tracks.py
        playlists.py
      dependencies/
        db.py
    core/
      config.py
      sanitizer.py
      db.py
    models/
      track.py
      playlist.py
    schemas/
      track.py
      playlist.py
    services/
      soundcloud.py
      yandex.py
  tests/
    test_tracks.py
  requirements.txt
  Dockerfile
  README.md
```

## Запуск

- Для локального запуска используйте команду:
  ```bash
  uvicorn app.main:app --reload
  ```
- Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

## Вклад

Pull requests и предложения приветствуются! Открывайте issues для обсуждения новых идей или багов.

## Лицензия

Проект распространяется под лицензией MIT.

## Авторы

- [xyzfbi](https://github.com/xyzfbi)
- [lyweze](https://github.com/lyweze)

## FAQ

**Q: Это продакшен-сервис?**  
A: Femin — это open-source проект для экспериментов и обучения, но его можно доработать для реального использования.

**Q: Как добавить новый источник музыки?**  
A: Реализуйте сервис в папке `services/` и подключите его в API.

**Q: Как интегрировать с фронтендом?**  
A: Используйте открытый API или готовый фронт [femin-front.netlify.app](https://femin-front.netlify.app/).

**Q: Как запустить тесты?**  
A: Выполните:
   ```bash
   python -m unittest discover tests
   ```

---

_Оригинальный репозиторий: [https://github.com/lyweze/femin](https://github.com/lyweze/femin)_
