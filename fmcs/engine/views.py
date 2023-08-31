from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TournamentForm, ParticipantForm
from .models import Tournament, Participant
from .utils.bracket_generator import generate_single_elimination_bracket
from glicko.models import Match


# Create your views here.

def event_view(request):
    events_list = Tournament.objects.all()
    reversed_events_list = sorted(events_list, key=lambda event: event.start_date, reverse=True)
    ongoing_upcoming_tournaments = [event for event in reversed_events_list
                                    if event.get_status() in ['Ongoing', 'Upcoming']]
    past_tournaments = [event for event in reversed_events_list if event.get_status() in ['Finished']]
    if ongoing_upcoming_tournaments:
        carousel_list = [event for event in ongoing_upcoming_tournaments]
    else:
        carousel_list = [event for event in past_tournaments[:5]]
    context = {
        'events_list': reversed_events_list,
        'carousel_list': carousel_list,
    }

    return render(request, 'explore.html', context=context)


def create_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            format = tournament.format

            if format == 'single_elimination':
                # Получаем участников с нужным турниром
                participants = Participant.objects.filter(tournament=tournament)
                num_participants = participants.count()

                # Вычисляем ближайшую степень двойки, которая больше или равна количеству участников
                power_of_two = 1
                while power_of_two < num_participants:
                    power_of_two *= 2

                # Вычисляем количество участников, которые нужно перенести на следующий раунд
                num_to_advance = num_participants - power_of_two // 2

                # Обновляем форму участников, чтобы перенести участников без пар на следующий раунд
                if num_to_advance > 0:
                    for participant in participants[:num_to_advance]:
                        participant.is_bye = True
                        participant.save()

                # Генерируем сетку для Single Elimination
                bracket, num_rounds = generate_single_elimination_bracket(num_participants)
                tournament.num_rounds = num_rounds

                # Дополнительный код для сохранения сетки в турнире
                # tournament.bracket = bracket

            tournament.save()
            return redirect('tournament_list')
        else:
            print(form.errors)  # Выведем ошибки в консоль для дальнейшего анализа
    else:
        form = TournamentForm()
    return render(request, 'create_tournament.html', {'form': form})


def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournament_list.html', {'tournaments': tournaments})


def add_participant(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.tournament = tournament
            participant.save()
            return redirect('tournament_detail', tournament_id=tournament_id)
    else:
        # Устанавливаем идентификатор турнира в качестве начального значения скрытого поля
        form = ParticipantForm(initial={'tournament': tournament_id})

    return render(request, 'add_participant.html', {'tournament': tournament, 'form': form})


def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    # if request.method == 'POST':
    #     form = ParticipantForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('tournament_detail', tournament_id=tournament_id)
    #
    #     new_start_date = request.POST.get('start_date')
    #     if new_start_date:
    #         tournament.start_date = new_start_date
    #         tournament.save()
    #         return redirect('tournament_detail', tournament_id=tournament_id)
    #
    # else:
    #     form = ParticipantForm()
    # match = Match.objects.get(event=tournament_id)
    matches_played = Match.objects.filter(event=tournament_id).count()
    participants = tournament.participants.all()

    context = {
        'tournament': tournament,
        'participants': participants,
        # 'match': match,
        'matches_played': matches_played,
        # 'form': form,
    }

    return render(request, 'tournament_detail.html', context=context)


def delete_participant(request, tournament_id, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    participant.delete()
    return redirect('tournament_detail', tournament_id=tournament_id)


def get_participants_data(request, tournament_id):
    participants = Participant.objects.filter(tournament__id=tournament_id).values('name')
    data = [{'name': participant['name']} for participant in participants]
    return JsonResponse(data, safe=False)
