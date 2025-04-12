CREATE TABLE tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL UNIQUE, -- путь к аудиофайлу
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица обложек
CREATE TABLE covers (
    cover_id SERIAL PRIMARY KEY,
    track_id INT REFERENCES tracks(track_id),
    image_path TEXT NOT NULL UNIQUE, -- путь к файлу обложки
    resolution VARCHAR(20), -- например "1200x1200"
    file_size INT -- размер в килобайтах
);