    document.getElementById('searchInput').addEventListener('input', function () {
        // Получаем значение поля поиска
        var keyword = this.value;

        // Отправляем AJAX-запрос на сервер
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/events/search/?keyword=' + encodeURIComponent(keyword), true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Обновляем содержимое блока с результатами поиска
                document.getElementById('search-results').innerHTML = xhr.responseText;
            }
        };
        xhr.send();
    });