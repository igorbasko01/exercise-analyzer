from typing import List


def extract_exercise_names(row: List[str], allowed_exercises=None) -> List[str]:
    _allowed_exercises = allowed_exercises or ['Chest', 'Squat', 'Row', 'Biceps W', 'Pullups']
    exercise_names = []
    for cell in row:
        if cell in _allowed_exercises:
            exercise_names.append(cell)

    if len(exercise_names) < len(_allowed_exercises):
        return []

    return exercise_names
