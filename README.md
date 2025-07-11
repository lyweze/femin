## НЕ САЖАЙТЕ МЕНЯ В ТЮРЬМУ
ЧЧМО НАХУЯ [АПИ](https://femin.onrender.com/) УБРАЛ ЧСВ 
# СОВРЕМЕННЫЙ web-сервис для прослушивания музыки, работающий на открытом API
![](https://github.com/user-attachments/assets/ad3cc5af-f50f-4f8c-973b-2f67f8cb3020)

## Structure

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

## Running the App

```bash
uvicorn app.main:app --reload
```
