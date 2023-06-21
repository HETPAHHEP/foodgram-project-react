# Foodgram — сайт рецептов ![Workflow-badge]

*Проект Foodgram «Продуктовый помощник».* Онлайн-сервис, в котором пользователи могут 
публиковать рецепты.

![Main page](docs/main-page.png)

### 🔥 Возможности

- Создавать свои рецепты
- Подписываться на авторов
- Добавлять чужие рецепты в избранное
- Добавлять чужие рецепты в корзину
- Скачивать список продуктов для блюд

### 👨‍💻 Технологии

[![Python][Python-badge]][Python-url]
[![DRF][DRF-badge]][DRF-url]
[![Gunicorn][Gunicorn-badge]][Gunicorn-url]
[![Postgres][Postgres-badge]][Postgres-url]
[![Docker][Docker-badge]][Docker-url]
[![Nginx][Nginx-badge]][Nginx-url]
[![Yandex-Cloud][Yandex-Cloud-badge]][Yandex-Cloud-url]
[![Github-Actions][Github-Actions-badge]][Github-Actions-url]

## ⚙ Начало Работы

Чтобы запустить копию проекта, следуйте инструкциям ниже.

### ⚠ Зависимости

- [Python 3.7+][Python-url]
- [Docker][Docker-url]


### 🏭 Запуск на сервере

1. **Обновите пакеты**
   
   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```

2. **Установите docker compose**
   
   ```bash
   sudo apt-get install docker.io
   sudo apt-get install docker-compose
   ```

3. **Перенести необходимые файлы**
   
   ```bash
   scp docker-compose.yml <username>@<host>:/home/<username>/
   scp nginx.conf <username>@<host>:/home/<username>/
   scp -r docs/ <username>@<host>:/home/<username>/docs/
   ```

4. **Создайте *dotenv-файл***

   ```bash
   touch .env
   ```

   ```dotenv
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=your.email.host
   EMAIL_PORT=555
   EMAIL=your@email.com
   EMAIL_PASSWORD=your-sending-email-password
   DJANGO_SECRET_KEY=your-django-secret
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password_here
   DB_HOST=host_here
   DB_PORT=5432
   DEBUG=True
   ALLOWED_HOSTS=localhost;127.0.0.1;backend;yourhost
   ```
   
   ###### **Секретный ключ можно сгенерировать [тут](https://djecrety.ir/)*

5. **Добавьте адрес в конфиг nginx**

   ```nginx
   server {
    listen 80;
    server_tokens off;
    server_name yourhost;
   ```

6. **Запустите контейнеры**

   ```bash
   sudo docker-compose up
   ```
   
7. **Завершите настройку Django**
   
   ```bash
   python manage.py migrate --no-input
   python manage.py collectstatic --no-input --clear
   python manage.py import_ingredients_json --no-input
   ```
   
   Запустите команды для выполнения миграций, сбора статики и
   добавления ингредиентов в контейнере


## 👀 Использование

![Usage-example](docs/demonstration.gif)

### 📖 API (Docs: [OpenAPI](docs/openapi-schema.yml))

Документация доступна по ссылке: http://localhost/api/docs/redoc.html

   ###### **Локальный эндпоинт*

## 🛠 Development

1. **Установите зависимости проекта**

    ```shell
    pip install -r requirements.txt
    ```

2. **Создайте *dotenv-файл* в корне настроек**

    ```dotenv
    EMAIL=your@email.com
    DJANGO_SECRET_KEY=django-insecure-c!1%u=@$f*u-*?9@jrst=k%-mziamu!voagve&lf=k7kqhn8qf
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password_here
    DB_HOST=localhost
    DB_PORT=5432
    ```

3. **Запустите dev-сервер**

    ```bash
    python manage.py runserver --settings=foodgram.dev-settings
    ```
   
---

<h5 align="center">
Автор проекта: <a href="https://github.com/HETPAHHEP">HETPAHHEP</a>
</h5>

<!-- MARKDOWN BADGES & URLs -->
[Python-badge]: https://img.shields.io/badge/Python-4db8ff?style=for-the-badge&logo=python&logoColor=%23ffeb3b

[Python-url]: https://www.python.org/

[Gunicorn-badge]: https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white

[Gunicorn-url]: https://gunicorn.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white

[Postgres-url]: https://www.postgresql.org/

[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white

[Docker-url]: https://www.docker.com/

[Nginx-badge]: https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white

[Nginx-url]: https://nginx.org

[DRF-badge]: https://img.shields.io/badge/Django_REST-f44336?style=for-the-badge&logo=django

[DRF-url]: https://www.django-rest-framework.org

[Yandex-Cloud-badge]: https://img.shields.io/badge/Yandex_Cloud-white?style=for-the-badge&logo=data%3Aimage%2Fwebp%3Bbase64%2CUklGRu4OAABXRUJQVlA4WAoAAAAQAAAAdwAAdwAAQUxQSGwJAAAN8J3t%2F%2F0%2FbW3dz6cA8ycFDP40MCQ3EIkGvDsfAxg596YBC40C2OR8GFGBYRQwQBkFRKQB%2F50GLNLA6%2BD3kwDpX0BETIA3%2F%2Ba9h7e377z%2Fzs1Ny99%2B%2BMfL%2F3j579%2B%2FdL8%2FfPzg8Q3MZdzevHvz329%2B%2BWDPn%2F%2F783vq5tePf70Z7GAXuX7z%2BNHDB8%2B%2Ffn5339w8%2FPMtlqtZO1swEd08%2Bs2ju2fP7%2B6R2w8%2FdDU7i5UIS5Pl8vFHj7776rt74tEnt7AWucwurqetJot99NHNF8%2Fugcd%2FPixyvV3EziKL7CA0D%2F74%2BOmzt%2BzhZ1hhmqwMdhZWC7EWkts%2Ff%2FCnr9%2BimyePt5jI1aywIyySy4S17Lz36Q9P796W33yGiLVr41grlh3syrSWWOjDP3z99K24%2BRLyyhZ2IK05WLS1tCNWW5ObP374wd2b9%2BjzLXvVCvLKZAorr1y0Ypj3%2F%2FrsizftyWOXud4sa1osS7BcJrkadtC883RPX75JN3%2BdZbEWwo5oihZLWBZkcrmQ9qf%2F%2Bbu7N%2Bf2ryNr7ey42o6ruRo72BGxrIbVJkve%2F8ufXrwpDz9jkstg2VlXrAsE7cKK7LhcIpP3nn3x9Zvx4LMRFtZakRbjwGRZYmKitdoZrNAvvvzmqzfh4WdeGYRYVsj15rK15LJFO5ClZdGX33718z343LQWVoSdlWWvws7a0VoXgixWLIt49u1XP9fDz7YDLVcn2mFnWaYlpIlox%2BUSLNhhTc%2B%2B%2Fvrnuf3M1VyN1bLDEiFBEFlzFqu1ooWsXP7lX1%2F8HLdfYrlsWbRD7JhCfnyiJXJ1xw7LCu%2F%2B5U93P8OXECaRJZizmp99scOOFTtzfbeff%2FzyJ3uCaRzLZa63ndXPlB0WLJdpxyIPfv30p%2FroFtEir1yLlfz8oSFapkVr8cd98dPcfmhhWmuxCFbe3KxFlp0hYZ98dfeTPCFWZskKFnmzg6lpxzTaufn045%2Fio7lsyeUOC3nTl1YjIlo7PH7wxY%2B7%2FdCCJgtLyBsfWjGx0A588uzuRz0hmMOOFYu9BZgsDbHE8s7nH%2F%2BY20fWImsHk5a8lS2xgyWm5vyz5z%2FiS5JlB3NsyVsbS5Zc5nLnySev9xEWYbVjifXWXA6ZLhbh8e2z13qCdrGDSEve5lwNpmXhydPX%2BQ1Wi6zlsuWtXyxaiLl9%2F7vX%2BMOELDuCJW%2F9zmISy4o%2FP33V7e3C2nF1rdyDOyIWsobHnr%2FiE5GEXOZeDJMdjMPiD59fu3nEcnVZy3QfXM2CMLEPXry88mvkerRD7stlx%2FWV0S9%2B%2B%2BzKR153kfs0grWamvrVNxe3761ltFqse8RiaYesrMcvXuKxiZaIxbo3Quywdszho2f4zQ5rWYudzXHftpYW1q%2B%2FwSMs0Q47O%2BYenSDBCg%2FvXnrEHFgh6D5pa2HaYXFz%2B8IvkctY5rhnI%2BxYa0frwfcee%2BWys8K6V147YvngWw%2Bw1s5KmNyryyLXVzz4%2FuYdImG5zP0aLMQy7f2XD7xmy3IPLwuLyM5%2B%2BcsJk8vQumfCRZgDvfeOqw25nns3TEuW1oNfXiyX62L30ZrasWTxzjsXYYol93BCWCt5%2F8aydlzNPb0Ldmjh9l1Xs9i9tTOtHVcn7%2B0QC1nWPdQOCcvO3GhCMIfcwzuurh3R3iXXF1nu4R0sWovFWixa2XEf5%2BpC7CChNYcdrHtnIZEl2j%2FetaydwSL3brBchqX%2F%2BoUQIVj3zuS1d9YdrLDWmnLvNtbCWu14%2Bbf3yWWS3NfZgmi9%2FPt%2Fi7Um1nQP7VgrtCz74R%2F%2FxA4ykfs4EqzsaC%2B%2Bf0B2pmj30%2BvGztp5%2Bbf3oR0W1r20XoHQvv%2F%2BgbVyOce6h3Ysa1muvnj5w3u5nsxZ1r2yEEFL%2FJ0XD%2BkKdojcq2lZdqys9YJvH8daa8Uy3SvsEBE78pzvH7J2liDkns1yuWjxghe3N1o7LBa5f5uQq%2FvhBS%2FvHtrx6mDdNyssa6Vv4ZtfFa1lrSX39Y7W%2Bubi2ccuE2kH615ZFlou8%2B3FyxePLy7XnGXHvbnsCGtdxHNXv%2F71tXY0wXRPRK4m1%2Ffs2le%2FubkitFYr9%2BbQWnvVD99de%2Fn9oytrWVpZ6z4YB0Je%2BbVXfv5Hi3bI9eRebC5XWMt6%2BqrvPI45MAXT27fSletB33nNp0%2BQ6%2B2KvP2txRKWHXz%2BOt%2Fd3q517erK9LZJiLWyg7vvX8cnT2JNEizydi92sXaEWJ947a9uH4uwK21lrbco1pqz49U9v3s9nzzJWgQrFnmrd2wlRhc%2B9COfe6Qd13eYs%2BPtnWh5dbC%2B9KM%2F%2Fuxmx%2BUEbXl7dwZpXclld1%2F9uLuvnnhlOy6D9TYsOxdrZ3J9%2BcRP%2BPnDxyOvXhZM6w1rx0KSdS3P%2FKQff37jsh3sTOMI6w2atGIZMVnr7quf5u6rP3dxPYjlTQ9iRTMHkqd%2B4s%2FP71likcsWYb0pLFMLLa9%2B6if%2F5DcPxTgwsrNgx8%2B%2FFnZoE1awluff%2FnQvP%2F7sFmHSmrMDO6yfK03CznK5FsndEz%2Fj3Z%2B%2BvGGRJXllaLHWT7AukMuVWCJX%2F%2Fa%2F%2FKwvPn%2BGhcZFF5MVkmUarWXBtNZFlpXl6vrHv%2FiZv%2Fn6L7negrVcttZCNC2JdpagadTKHGs4L3%2FnZ3%2F2b38Jk1wmcrUddiE7FpZXtiKXa4eF%2FON33sBnz%2F8SYoLlckXI1R0scrnY8ZrtILQffueNfPZ%2F%2F8%2BNw86m5XKOqwvTDjtYO5KVq9POzrJW%2B8%2BPvKFf%2F%2BuXt%2BwIudqwyGUyjRKLsNghFmT%2F%2BZE39sWfvrzVaGEh5OoyCmtagiUr2DFi%2F%2F8P3uC73374RyK0yfKaO2axQztY1tCgVhb%2F%2B%2F95o18%2B3SfvWqwdI2tZhAytFkRed2HH3cfe%2BC%2Be%2FfWWlVaQCAvCzhLLXm9nZ86%2BeeotvPvgoz%2F%2B4kAsr5u1FiF2rKx1rR35x7%2FM2%2FnJN3%2F6Hy1Lrq4LO5JFC3bMERM71hdfeGvvPvmvT993ua40IZc7lss0Zy6D%2BLc%2FeKu%2F%2FtPjJ7ctIyuXa9mxJsuSphF893Te9mdPH%2F%2Fh4WqR68nOHJfRDqKxvnvqXnz2xbsffbjj%2BmIRTctllqu9%2FNcv3ZvfPXv%2BwYePLIRctoN1sVx9%2Bf0nd%2B7Vu%2B%2Be%2Ff3R7%2F75BhYsseNyab38%2Bvl37uG75399%2FvDBB49ugh3YGZG%2Ff%2Fsf3965v7%2F7%2FtvnHj68eXDzT%2B%2B8t3j5w8u7f%2Fz97sWdNx9WUDggXAUAAJAeAJ0BKngAeAA%2BUSCNRCGhDAYCUAwCgliA7AbNLQ6DbkvwOY67rmX8Heerzz46PUT5hP61dI7zI%2FsR%2ByXu5%2F4z9u%2FdP%2FdfUA%2FqP9261v0EP4j%2F0utL%2Fdz0sMxw%2BiXk3PwTxZyUqCGheVKWxn33yCPSAWP3j7Fvj2AfE1Y6uXqmZBrH64qT7nkIujtzPqMvFT9SFCf8RJ2mofYEk6j0jIWUCPjLe72KLLkMeFidcuw7S1mNeeDzNPWAyVYa4fDPeYxp6fPhzcpISDoSdWnoE7lwG%2FY6OpiNW6ukdyZVDssazGrAWDqZkO%2F7BDdYrRxho4TzsP%2BWJIN4d3qQ0AAA%2Fv4%2BwJz8nuZxoRNYR%2BR8lb1LnPHV%2B15QOYjaLgKOLZoTddtq9KwhOhpy3eD%2FriKYCtt64pz%2F8X7KXYu1fKdlYe%2BMB4RzllzkSIvow79AIaGLKuuZH%2B4Ks0hh6Pb7acIYEQAXj9WeasCftad%2Fl65Vt12cF8USQAkT7EwCACH%2Fbhd2YiS3wm8p%2B8WE982swFU3nptBZZWvAej2Rh0CgCU7Jy0%2FwlcBNwNmdK0hHY1K2EcjopTlAFYMUELjiSp8PiVz66zFxPsAD2d3HrsAOEkznsBO0fWOGexNEzkH8VIrB5n8Xtb9dABcENnwQu0lCUqMNr4W9Ac0QYEc7jRrgH7IegYZ7MOZb%2FXr%2FqCXyJVXgPbOl1C%2Bh72cNn8T6VIRW6SpKCaMF58paNmpsG%2FGBhJ90EgqWzK5LE1HenRdQfVipJpktA7zZoQJhqFdGTlCoT2GXOAcfi0ygRXEoTm55Psmtf7SDCRs7WtvAzxKgl7fa00%2FlniW7Gw8WMM7X%2BGdeJogIQ5qg0WtEbPo3ypiBgeB2%2BAvpxvg%2FA0lAG6F3Up%2Bh7fmeWiaX0fjD2G5sdQRmCvF4E9QcG18N0DVPtCbrbR%2BvtiJSj02eBMq1CmLumgWslGVjky4D0%2FzHLwMzfD3re1MWxXw5InF3E5N%2BoM7gPV%2BA3%2B65ktkvCy9q3F9ODSbe1GuWT0KxcyeEpsHMjhQmcrUZZ0LJCyAFsVXcUXJYFMAaAsg5PwNjbSXTUmlB%2FdAqR%2B%2FdbGYsoQC4zJWsnRFlgCQoRmmeDDqbtie0bXywFSDRfoz11iuoGmN2RZ7%2FozjVF3pw%2FrsfTZSUrt4Kkt2vCt4Djf8%2FwznAL2nbtA%2FxAOTvxX3tMz%2B5aDmFerKmWlYs14AJ31XwWFtQtmrUFGXJbKOkD%2FWwfjx20CqC1pewd4VLbaO5aslN2Pp%2BtoHu1RN4mhamn799dVOcG8KFmMbrTmBxbmycn3lq2ZE%2FzC09EG7dPoFsTHwLHZsmL5CpPt0F%2FlBdmfFS2CN4n8lQ5y%2FhBU8TfkzCK%2B1H1KczwzzjMAslrLNFVhof0rrLj2DMw6OFMfBj55ZivUdSx6dcsk044O6AlzaIhRRtACNo%2BfrKlaXmOH5pumj4vdOGSeHzun5%2B2sEvqr%2B0Osv4e6c8ofDQFadHq3oboL%2FYK7qJ9NYuORo%2B%2B%2FfVQjKYNabJqEjwbz1cYRYlQStYyftJ8xOSgjLrivDnpLXSqNmnClTj2ZvkmOATJalmHauTKdgjsZ7QhP%2Fr4ZqNgn3q4uW8hF5uVhiRC3Y8pX%2Fp6Ggv2zdTDZ9HSiV50xnH%2Bv4xR6Ntaj2Cb%2BbmBDbRxZXUrsMn3wPCS9lBB3EpXZrDzS52Jr5NmlB%2Fp0JZg%2FMyQdhdM0cEsBPdKnzMsJ1gLRwiL1UhrX73rJeQnTvikuaV%2F1Mn%2BoYezJS21l0n%2FwLMsL4HQk%2Bd547fvL%2FiHdmF6%2BORb5weg0IU27GXAbeMwyNCb94IALJdoAAAAA%3D

[Yandex-Cloud-url]: https://cloud.yandex.ru

[Github-Actions-badge]: https://img.shields.io/badge/Github_Actions-%239c27b0?style=for-the-badge&logo=github%20actions&logoColor=white

[Github-Actions-url]: https://github.com/features/actions

[Workflow-badge]: https://img.shields.io/github/actions/workflow/status/HETPAHHEP/foodgram-project-react/foodgram-workflow.yml?style=for-the-badge&logo=github&label=Foodgram%20Workflow
