//document.addEventListener('DOMContentLoaded', function () {
//    // Запрос на отображение всех участников при открытии страницы
//    var xhr = new XMLHttpRequest();
//    xhr.open('GET', '/fmcs/search/', true);
//    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
//    xhr.onreadystatechange = function () {
//        if (xhr.readyState === 4 && xhr.status === 200) {
//            document.getElementById('search-results').innerHTML = xhr.responseText;
//        }
//    };
//    xhr.send();
//
//    // Обработчик события для фильтрации по keyword
//    document.getElementById('searchInput').addEventListener('input', function () {
//        var keyword = this.value;
//        console.log(keyword)
//        // Отправляем AJAX-запрос на сервер с параметром keyword
//        var xhr = new XMLHttpRequest();
//        console.log(xhr)
//        var url = '/fmcs/search/?keyword=' + encodeURIComponent(keyword);
//        console.log(url)
//        xhr.open('GET', url, true);
//        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
//        xhr.onreadystatechange = function () {
//            if (xhr.readyState === 4 && xhr.status === 200) {
//                document.getElementById('search-results').innerHTML = xhr.responseText;
//            }
//        };
//        xhr.send();
//    });
//});
//document.addEventListener('DOMContentLoaded', function () {
//    // Обработчик события для фильтрации по keyword
//    document.getElementById('searchInput').addEventListener('input', function () {
//        var keyword = this.value;
//        console.log(keyword)
//        // Отправляем AJAX-запрос на сервер с параметром keyword
//        var xhr = new XMLHttpRequest();
//        console.log(xhr)
//        var url = '/ranking/search/?keyword=' + encodeURIComponent(keyword);
//        console.log(url)
//        xhr.open('GET', url, true);
//        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
//        xhr.onreadystatechange = function () {
//            if (xhr.readyState === 4 && xhr.status === 200) {
//                document.getElementById('search-results').innerHTML = xhr.responseText;
//            }
//        };
//        xhr.send();
//    });
//
//    // Запрос на отображение всех участников при открытии страницы
//    var xhr = new XMLHttpRequest();
//    xhr.open('GET', '/ranking/search/', true);
//    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
//    xhr.onreadystatechange = function () {
//        if (xhr.readyState === 4 && xhr.status === 200) {
//            document.getElementById('search-results').innerHTML = xhr.responseText;
//        }
//    };
//    xhr.send();
//});
document.addEventListener('DOMContentLoaded', function () {
    var searchInput = document.getElementById('searchInput');
    var searchResults = document.getElementById('search-results');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/fmcs/search/', true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    // Функция для отправки запроса
    function sendRequest() {
        var keyword = searchInput.value;
        var url = '/fmcs/search/?keyword=' + encodeURIComponent(keyword);

        xhr.open('GET', url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                searchResults.innerHTML = xhr.responseText;
            }
        };
        xhr.send();
    }

    // Обработчик события для фильтрации по keyword
    searchInput.addEventListener('input', function () {
        clearTimeout(this.timer);
        this.timer = setTimeout(sendRequest, 800); // Задержка в 500 миллисекунд (половина секунды)
    });

    // Инициализация поиска при загрузке страницы
    sendRequest();
});
