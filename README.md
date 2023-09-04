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

Сайт показывает текущий рейтинг, турниры турнирной площадки. Пользователи могут редактировать и создавать свои команды
для
участия в турнирах. Поддерживается создание и редактирование профилей пользователей.

---

## Технологии

- _Django Framework_
- _PostgreSQL_
- _AJAX, HTML5, CSS_
- _Django Templates_

---

## Используемые библиотеки

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