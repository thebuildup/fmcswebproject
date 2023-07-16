from engine.models import Participant


def generate_single_elimination_bracket(tournament_id):
    bracket = []
    num_rounds = 0

    # Получаем участников с нужным турниром
    participants = Participant.objects.filter(tournament__id=tournament_id)
    num_participants = participants.count()

    # Проверяем, является ли количество участников степенью двойки
    if num_participants & (num_participants - 1) != 0:
        raise ValueError("Количество участников должно быть степенью двойки")

    # Создаем список участников в формате [участник1, участник2, участник3, ...]
    participants_list = [participant.name for participant in participants]

    # Генерируем первый раунд
    first_round = []
    for i in range(0, len(participants_list), 2):
        match = (participants_list[i], participants_list[i + 1])
        first_round.append(match)
    bracket.append(first_round)
    num_rounds += 1

    # Генерируем последующие раунды до определения победителя
    while len(first_round) > 1:
        next_round = []
        for match in first_round:
            winner = input(f"Победитель матча {match[0]} vs {match[1]}: ")
            next_round.append(winner)
        bracket.append(next_round)
        first_round = next_round
        num_rounds += 1

    return bracket, num_rounds


if __name__ == "__main__":
    # Вместо того, чтобы пользователь вводил количество участников,
    # теперь нужно передать идентификатор турнира в качестве аргумента
    tournament_id = 1  # Здесь замените на нужный идентификатор турнира
    bracket, num_rounds = generate_single_elimination_bracket(tournament_id)

    print("Сетка Single Elimination:")
    for i, round in enumerate(bracket):
        print(f"Раунд {i + 1}: {round}")
