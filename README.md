# Курсовая работа
Разработка интерактивного помощника для осуществления розничных покупок

## Структура проекта
Папки или файлы, помеченные как неинформативные, являются черновиками или заметками, не имеющими какой-либо полезной информации

### /old, debug.py, notes.md
Неинформативно 

### app.py
main веб-приложения

### utils содержит различные целевые модули:
- config.py - инициализация глобальных справочных переменных (стоп-слова, единицы измерения и т.д.)
- db.py - функции для работы с БД
- parser.py - функции по обработке запросов
- response.py - функции по формированию ответов в формате json
- suggest.py - функции по формированию рекомендаций 

### /notebooks
- eda_parsing.ipynb - парсинг сайта eda.ru 
- eda_preprocessing.ipynb - обработка датасета с eda.ru
- eda_recs.ipynb - рекомендации на основе датасета с eda.ru

### data/db.sql
Здесь сохранен SQL код для создания необходимых таблиц в PostgreSQl

### /paper
Отчет