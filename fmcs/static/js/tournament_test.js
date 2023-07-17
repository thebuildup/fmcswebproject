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
		fetchParticipantsData(generateBracket);
        } else {
            // Если выбрана вкладка "Участники", показываем список участников и скрываем остальные вкладки
            $("#matches").hide();
            $("#grid").hide();
            $("#participants").show();

            // Получить и отобразить данные участников
        }
    });

    // Функция для генерации сетки с помощью jQuery Bracket
    // Функция для получения данных участников турнира с помощью AJAX
function saveFn(data, userData) {
  var json = jQuery.toJSON(data)
  $('#saveOutput').text('POST '+userData+' '+json)
  /* You probably want to do something like this
  jQuery.ajax("rest/"+userData, {contentType: 'application/json',
                                dataType: 'json',
                                type: 'post',
                                data: json})
  */
}

function generateBracket(data) {
  const powerOfTwo = Math.pow(2, Math.ceil(Math.log2(data.length)));
  const fillCount = powerOfTwo - data.length;

  for (let i = 0; i < fillCount; i++) {
    data.push({ name: null });
  }

var placeData = {
            teams: data.map(function(participant) {
//                return [participant.name, null];
                return [participant.name];
            }),
            results: []
        };

var container = $('#bracket-container');
    container.bracket({
        init: placeData,
        save: saveFn,
        /* You can also inquire the current data */
        var output = container.bracket('data');
        $('#dataOutput').text(jQuery.toJSON(output));
    });

$('div#bracket-container').bracket({
            init: placeData,
            teamWidth: 150,
            scoreWidth: 30,
            matchMargin: 30
        });
}



function fetchParticipantsData(callback) {
        var tournamentId = $('#bracket-container').data('tournament-id');
        $.ajax({
            url: `get_participants_data/`,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
            	console.log(data)
                // Вызов функции обратного вызова и передача данных участников
                if (typeof callback === 'function') {
                console.log(data)
                    callback(data);
                }
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при получении данных участников:', error);
            }
        });
    }



});
