<p align="center">
  <p align="center">
    <a href="http://fmchamps.vh104.hosterby.com/" target="_blank">
      <img src="https://github.com/thebuildup/fmcswebproject/blob/master/fmcs/static/images/logo_fmcs.png" alt="FMCS Online" height="72">
    </a>
  </p>
  <p align="center">
    Веб-сайт для турнирной площадки FMCS.
  </p>
</p>

## **Предупреждение об активном этапе разработки**

Данный репозиторий является демонстрацией для защиты проекта IT-Academy по курсу "Комплексный курс по разработке
веб-приложений на Python"

### Автор: Рудаков Роман

---

# **Django FMCS Online**

Это специально разработанное веб-приложение для турнирной площадки FMCS с помощью Django.

Ссылка на проект на хостинге - http://fmchamps.vh104.hosterby.com/

---

## Резюме проекта

Сайт показывает текущий рейтинг (Glicko-2), турниры турнирной площадки. Пользователи могут редактировать и создавать
свои команды для участия в турнирах и ладдерах, собирать свои составы из базы данных игроков Football Manager 2023.

**Рейтинговая система Glicko-2**

- Улучшенная система рейтинга с учётом частоты игр команды
- Дополнительные коэффициенты при расчёте рейтинга (частота игр, стабильность результатов)
- Автоматический подсчёт рейтинга для нового рейтингового периода
- Сохранение статистики рейтинга по рейтинговым периодам

**Расширенная статистика**

- Сохранение статистики команды
- Возможность хранить данные статистики по каждому матчу (1-5 матчей в противостоянии)
- Сохранение истории противостояний между командами

---

### Реализовано

- _Рейтинговая система Glicko-2_
- _Создание и редактирование команд, пользователей_
- _Создание и редактирование турниров_
- _Чтение pgn-файлов с результатами матчей и автоматическое добавление всей информации в БД_

---

### Будущие обновления

- _Турнирный движок (в разработке)_
- _Открытые ладдеры_
- _Возможность набирать свой состав из базы данных игроков Football Manager (в разработке)_
- _Расширенная статистика_

---

### Технологии

- _Django Framework_
- _PostgreSQL_
- _AJAX, HTML5, CSS_
- _Django Templates_

---

### Используемые библиотеки

- _django-countries_
- _django-import-export_
- _django-dotenv_
- _django-resized_
- _psycopg2-binary_

---

## Запуск проекта

Чтобы запустить этот проект, вам следует начать с установки Python на вашем компьютере. Рекомендуется создать
виртуальная среда для отдельного хранения зависимостей ваших проектов. Вы можете установить virtualenv с помощью:

```
pip install virtualenv
```

Клонируйте или загрузите этот репозиторий и откройте его в любом редакторе. В терминале (mac/linux) или терминале
Windows
выполните следующую команду в базовом каталоге этого проекта

```
virtualenv env
```

Это создаст новую папку env в каталоге вашего проекта. Затем активируйте его с помощью этой команды:

```
source env/bin/active
```

Затем установите зависимости проекта с помощью

```
pip install -r requirements.txt
```

Теперь вы можете запустить проект с помощью этой команды

```
python manage.py runserver
```

---

<div align="center">

<i>Где вы можете найти нас:</i><br>

<a href="https://twitter.com/FMChampSeries" target="_blank"><img src="https://img.shields.io/badge/Twitter-%231877F2.svg?&style=flat-square&logo=twitter&logoColor=white" alt="Twitter"></a>

</div>