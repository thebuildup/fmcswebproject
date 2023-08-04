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
//document.addEventListener('DOMContentLoaded', function () {
//    // Function to hide all players and display the preloader
//    function hidePlayersShowPreloader() {
//        document.getElementById('search-results').innerHTML = ''; // Clear the search results
//        document.getElementById('js-preloader-result').classList.remove('loaded');
//    }
//
//    // Function to display the preloader
//    function showPreloader() {
//        document.getElementById('js-preloader-result').classList.remove('loaded');
//    }
//
//    // Function to hide the preloader
//    function hidePreloader() {
//        document.getElementById('js-preloader-result').classList.add('loaded');
//    }
//
//    // Show all players on page load
//    var xhr = new XMLHttpRequest();
//    xhr.open('GET', '/ranking/search/', true);
//    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
//    xhr.onreadystatechange = function () {
//        if (xhr.readyState === 4 && xhr.status === 200) {
//            document.getElementById('search-results').innerHTML = xhr.responseText;
//            hidePreloader(); // Hide the preloader once the players are loaded
//        }
//    };
//    xhr.send();
//
//    // Event listener for the search input field
//    document.getElementById('searchInput').addEventListener('input', function () {
//        var keyword = this.value;
//
//        // If the keyword is not empty, hide players and show the preloader
//        if (keyword.trim() !== '') {
//            hidePlayersShowPreloader();
//        } else {
//            // If the keyword is empty, hide the preloader and show all players
//            hidePreloader();
//            var xhr = new XMLHttpRequest();
//            xhr.open('GET', '/ranking/search/', true);
//            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
//            xhr.onreadystatechange = function () {
//                if (xhr.readyState === 4 && xhr.status === 200) {
//                    document.getElementById('search-results').innerHTML = xhr.responseText;
//                    hidePreloader(); // Hide the preloader once the players are loaded
//                }
//            };
//            xhr.send();
//        }
//
//        // Send AJAX request to the server with the keyword
//        var xhr = new XMLHttpRequest();
//        var url = '/ranking/search/?keyword=' + encodeURIComponent(keyword);
//        xhr.open('GET', url, true);
//        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
//        xhr.onreadystatechange = function () {
//            if (xhr.readyState === 4 && xhr.status === 200) {
//                document.getElementById('search-results').innerHTML = xhr.responseText;
//                hidePreloader(); // Hide the preloader once the search results are loaded
//            }
//        };
//        xhr.send();
//    });
//});

