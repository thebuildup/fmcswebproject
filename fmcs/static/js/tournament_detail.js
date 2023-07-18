$(document).ready(function() {
    // Обработка события переключения вкладок
    $('.nav-tabs a').on('shown.bs.tab', function(event) {
        var target = $(event.target).attr('href');
        if (target === "#matches") {
            // Ваш код для отображения матчей
            $("#participants").hide(); // Скрываем список участников
            $("#grid").hide();
            $("#matches").show(); // Показываем вкладку с матчами
        } else if (target === "#grid") {
            $("#participants").hide(); // Скрываем список участников
            $("#matches").hide();
            $("#grid").show(); // Показываем вкладку с таблицей

            // Вызов функции для генерации сетки с помощью jQuery Bracket
            generateBracket();
        } else {
            // Если выбрана вкладка "Участники", показываем список участников и скрываем остальные вкладки
            $("#matches").hide();
            $("#grid").hide();
            $("#participants").show();

            // Получить и отобразить данные участников
            var tournamentId = $('#bracket-container').data('tournament-id');
            fetchParticipantsData(tournamentId);
        }
    });

    // Функция для генерации сетки с помощью jQuery Bracket
    function generateBracket() {
        // Пример данных участников, полученных с сервера (замените данными из AJAX-запроса)
        if (!teams) {
            console.error("No teams data provided.");
            return;
        }

        var place_data = {
            teams: teams,
            results: []
        };
        // Формируем данные для генерации сетки
        var teams = participantsData.map(function(participant) {
            return [participant.name, null];
        });

        var place_data = {
            teams: teams,
            results: []
        };

        // Используем библиотеку jQuery Bracket для генерации сетки на странице
        $('#bracket-container').bracket({
            init: place_data,
            teamWidth: 150,
            scoreWidth: 30,
            matchMargin: 30
        });
    }

    // Функция для получения данных участников турнира с помощью AJAX
    function fetchParticipantsData(tournamentId) {
        $.ajax({
            url: `get_participants_data/`,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // Обработка данных участников
                var formattedData = formatParticipantsData(data);
                // Передаем отформатированные данные участников для генерации сетки
                generateBracket(formattedData);
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при получении данных участников:', error);
            }
        });
    }

	    function formatParticipantsData(data) {
        // Преобразовать данные участников в необходимый формат без кавычек
        return data.map(function(participant) {
            return { name: participant.name };
        });
    }


    // Функция для генерации сетки с данными участников
    function generateBracketWithData(participantsData) {
        var teams = participantsData.map(function(participant) {
            return [participant.name, null];
        });

        var place_data = {
            teams: teams,
            results: []
        };

        // Используем библиотеку jQuery Bracket для генерации сетки на странице
        $('#bracket-container').bracket({
            init: place_data,
            teamWidth: 150,
            scoreWidth: 30,
            matchMargin: 30
        });
    }

    // ... Остальной код
});
