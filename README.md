# Coursework
Development of an interactive shopping assistant for retail purchases

## Ideas
### I stage
1. Алиса; Яндекс.Диалоги; Навыки
2. Цены из Яндекс.Маркет
3. Покупки с Алисой: https://yandex.ru/alice/shopping-list

### II stage
* Алиса не умеет работать со встроенным функционалом, навык обособлен -> разрабатывать свой список покупок
    * Алиса не позволяет использовать встроенный функционал при работе с Навыком. По сути при создании Навыка мы находимся в диалоге, где Алиса выступает в роли приемника вопроса + отсылает ответ. 
        1. Придется заново реализовать список   покупок
        2. Она не умеет работать в автономном   режиме и при этом функция должна присылать ответ за не более 3 секунд
        3. Не получится определить локацию

### III stage
* Посмотреть реализации с фотками чеков
* ТГ бот для покупок
* Приложение на IOS для покупок

### IV stage
* ITEM-to-ITEM Recommendations
    * Подход 1. Товары из той же категории
    * Подход 2. На основе рецептов

## Plans
### Bot
1. Вести список покупок
2. Напоминать о покупках
3. Отслеживать общую стоимость и вид товара
4. Предлагать другие покупки на основе выбранных
5. Отслеживать скоропортящиеся и напоминать о необходимости их купить
6. Отслеживать скидки и акции

### Features
1. ITEM-to-ITEM recommendation system

## Workflow
### Тест функционала Алисы
* Алиса умеет:
    1. Вести список покупок
    2. Средняя цена конкретного товара в Яндекс.Маркет по отдельному запросу

## Issues
* Можно ли работать совместно со встроенным функционалом Алисы или придется будет взять реализованный навык?
    * Нельзя

## Datasets
* https://dominikschmidt.xyz/simplified-recipes-1M/
