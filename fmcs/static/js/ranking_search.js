document.addEventListener('DOMContentLoaded', function () {
    // Запрос на отображение всех участников при открытии страницы
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/ranking/search/', true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('search-results').innerHTML = xhr.responseText;
        }
    };
    xhr.send();

    // Обработчик события для фильтрации по keyword
    document.getElementById('searchInput').addEventListener('input', function () {
        var keyword = this.value;

        // Отправляем AJAX-запрос на сервер с параметром keyword
        var xhr = new XMLHttpRequest();
        var url = '/ranking/search/?keyword=' + encodeURIComponent(keyword);
        xhr.open('GET', url, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                document.getElementById('search-results').innerHTML = xhr.responseText;
            }
        };
        xhr.send();
    });
});