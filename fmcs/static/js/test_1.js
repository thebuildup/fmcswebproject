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

            // Вызов функции для получения данных участников и генерации сетки
            fetchParticipantsData();
        } else {
            // Если выбрана вкладка "Участники", показываем список участников и скрываем остальные вкладки
            $("#matches").hide();
            $("#grid").hide();
            $("#participants").show();

            // Получить и отобразить данные участников
        }
    });

    // Функция для генерации сетки с помощью jQuery Bracket
    function generateBracket(data) {

    	if (!data || data.length === 0) {
            console.error('Нет данных участников.');
            return;
        }

        const powerOfTwo = Math.pow(2, Math.ceil(Math.log2(data.length)));
        const fillCount = powerOfTwo - data.length;

        for (let i = 0; i < fillCount; i++) {
            data.push({ name: null });
        }

        var placeData = {
            teams: data.map(function(participant) {
//                return [participant.name, null];
                return [participant.name, null];
            }),
            results: []
        };
		console.log(placeData)
        var container = $('#bracket-container');
        container.bracket({
            init: placeData,
            save: saveFn,
        });

        // В этом месте вы можете делать другие операции с данными, если необходимо
    }

    function fetchParticipantsData() {
        var tournamentId = $('#bracket-container').data('tournament-id');
        $.ajax({
            url: `get_participants_data/`,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // Вызов функции генерации сетки и передача данных участников
                generateBracket(data);
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при получении данных участников:', error);
            }
        });
    }

    // Функция для сохранения данных в POST запросе (если нужно)
    function saveFn(data, placeData) {
        var json = jQuery.JSON.stringify(data);
        $('#saveOutput').text('POST ' + placeData + ' ' + json);
        /* You probably want to do something like this
        jQuery.ajax("rest/"+userData, {contentType: 'application/json',
                                        dataType: 'json',
                                        type: 'post',
                                        data: json})
        */
    }
});
