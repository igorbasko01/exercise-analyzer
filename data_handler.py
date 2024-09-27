from datetime import datetime
from typing import List, Callable, Optional, Tuple


def extract_exercise_names(row: List[str], allowed_exercises=None) -> List[str]:
    _allowed_exercises = allowed_exercises or ['Chest', 'Squat', 'Row', 'Biceps W', 'Pullups']
    exercise_names = []
    for cell in row:
        if cell in _allowed_exercises:
            exercise_names.append(cell)

    if len(exercise_names) < len(_allowed_exercises):
        return []

    return exercise_names


def extract_weights_from_formula(formula: Optional[str]) -> str:
    if not formula:
        return ''
    return formula.split('*')[0].replace('=', '').replace('(', '').replace(')', '')


def extract_sets_and_reps_from_formula(formula: Optional[str]) -> List[str]:
    if not formula:
        return []
    operands = formula.split('*')[1:]
    if len(operands) == 1 and operands[0].startswith('('):
        sets = _extract_specific_reps(operands[0])
        return sets
    elif len(operands) == 2:
        first, second = int(operands[0]), int(operands[1])
        sets, reps = str(min(first, second)), str(max(first, second))
        return [str(reps)] * int(sets)
    else:
        return []


def _extract_specific_reps(formula: str) -> List[str]:
    return formula.replace('(', '').replace(')', '').split('+')


def explode_exercises(input_rows: List[List[str | datetime]],
                      header_row: List[str],
                      weights_extractor: Callable[[str], str] = extract_weights_from_formula,
                      sets_reps_extractor: Callable[[str], List[str]] = extract_sets_and_reps_from_formula,
                      alternative_exercise_names: List[str] = None) -> List[List[str]]:

    alternative_exercise_names = alternative_exercise_names or ['Bench Press', 'Squat', 'Bent Over Row',
                                                                'EZ Barbell Curl', 'Pullups']
    for row in input_rows:
        if not row[0] or not isinstance(row[0], datetime):
            continue
        date = row[0].strftime('%Y-%m-%d')
        for i, exercise in enumerate(header_row[1:]):
            weights = weights_extractor(row[i + 1])
            sets = sets_reps_extractor(row[i + 1])
            for reps in sets:
                yield [date, alternative_exercise_names[i], weights, reps]
