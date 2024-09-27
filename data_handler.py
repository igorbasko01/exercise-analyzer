from datetime import datetime
from typing import List, Callable


def extract_exercise_names(row: List[str], allowed_exercises=None) -> List[str]:
    _allowed_exercises = allowed_exercises or ['Chest', 'Squat', 'Row', 'Biceps W', 'Pullups']
    exercise_names = []
    for cell in row:
        if cell in _allowed_exercises:
            exercise_names.append(cell)

    if len(exercise_names) < len(_allowed_exercises):
        return []

    return exercise_names


def explode_exercises(input_rows: List[List[str | datetime]],
                      header_row: List[str],
                      weights_extractor: Callable[[str], str],
                      reps_extractor: Callable[[str], str],
                      alternative_exercise_names: List[str]) -> List[List[str]]:
    for row in input_rows:
        if not row[0] or not isinstance(row[0], datetime):
            continue
        date = row[0].strftime('%Y-%m-%d')
        for i, exercise in enumerate(header_row[1:]):
            weights = weights_extractor(row[i + 1])
            reps = reps_extractor(row[i + 1])
            yield [date, alternative_exercise_names[i], weights, reps]