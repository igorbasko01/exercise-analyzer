import datetime
import unittest
from typing import List, Tuple

from data_handler import extract_exercise_names, explode_exercises, extract_weights_from_formula, \
    extract_sets_and_reps_from_formula


class DataHandlerTests(unittest.TestCase):
    def test_extract_exercise_names(self):
        exercise_names = extract_exercise_names(
            ['Date', 'Chest', 'Squat', 'Row', 'Biceps W', 'Pullups', 'col1', 'col2'])
        self.assertEqual(exercise_names, ['Chest', 'Squat', 'Row', 'Biceps W', 'Pullups'])

    def test_extract_exercise_names_empty(self):
        exercise_names = extract_exercise_names([])
        self.assertEqual(exercise_names, [])

    def test_extract_exercise_names_missing_all_exercises(self):
        exercise_names = extract_exercise_names(['Date', 'col1', 'col2'])
        self.assertEqual(exercise_names, [])

    def test_extract_exercise_names_missing_single_exercise(self):
        exercise_names = extract_exercise_names(['Date', 'Chest', 'Row', 'Biceps W', 'Pullups', 'col1'])
        self.assertEqual(exercise_names, [])

    def test_explode_exercises(self):
        def sample_weights_extractor(formula: str) -> Tuple[str, str]:
            return formula, formula

        def sample_reps_extractor(formula: str) -> List[str]:
            return ['3']

        header_row = ['Date', 'Chest', 'Squat', 'Row', 'Biceps W', 'Pullups']
        alternative_exercise_names = ['Bench Press', 'Leg Press', 'Bent Over Row', 'Barbell Curl', 'Pullups']
        input_rows = [[datetime.datetime(2023, 10, 25), 'weights1', 'weights2', 'weights3', 'weights4', 'weights5']]
        actual_rows = explode_exercises(input_rows, header_row, sample_weights_extractor, sample_reps_extractor,
                                        alternative_exercise_names)
        expected_rows = [['2023-10-25', 'Bench Press', 'weights1', 'weights1', '3'],
                         ['2023-10-25', 'Leg Press', 'weights2', 'weights2', '3'],
                         ['2023-10-25', 'Bent Over Row', 'weights3', 'weights3', '3'],
                         ['2023-10-25', 'Barbell Curl', 'weights4', 'weights4', '3'],
                         ['2023-10-25', 'Pullups', 'weights5', 'weights5', '3']]
        self.assertEqual(list(actual_rows), expected_rows)

    def test_explode_exercises_skip_row_starts_with_not_a_date(self):
        def sample_weights_extractor(formula: str) -> str:
            return formula

        def sample_reps_extractor(formula: str) -> List[str]:
            return ['3']

        header_row = ['Date', 'Chest', 'Squat', 'Row', 'Biceps W', 'Pullups']
        alternative_exercise_names = ['Bench Press', 'Leg Press', 'Bent Over Row', 'Barbell Curl', 'Pullups']
        input_rows = [[None, 'weights1', 'weights2', 'weights3', 'weights4', 'weights5']]
        actual_rows = explode_exercises(input_rows, header_row, sample_weights_extractor, sample_reps_extractor,
                                        alternative_exercise_names)
        expected_rows = []
        self.assertEqual(list(actual_rows), expected_rows)

    def test_explode_exercises_explode_sets(self):
        def sample_weights_extractor(formula: str) -> Tuple[str, str]:
            return formula, formula

        def sample_reps_extractor(formula: str) -> List[str]:
            return ['3', '4', '5']

        header_row = ['Date', 'Chest', 'Squat', 'Row', 'Biceps W', 'Pullups']
        alternative_exercise_names = ['Bench Press', 'Leg Press', 'Bent Over Row', 'Barbell Curl', 'Pullups']
        input_rows = [[datetime.datetime(2023, 10, 25), 'weights1', 'weights2', 'weights3', 'weights4', 'weights5']]
        actual_rows = explode_exercises(input_rows, header_row, sample_weights_extractor, sample_reps_extractor,
                                        alternative_exercise_names)
        expected_rows = [['2023-10-25', 'Bench Press', 'weights1', 'weights1', '3'],
                         ['2023-10-25', 'Bench Press', 'weights1', 'weights1', '4'],
                         ['2023-10-25', 'Bench Press', 'weights1', 'weights1', '5'],
                         ['2023-10-25', 'Leg Press', 'weights2', 'weights2', '3'],
                         ['2023-10-25', 'Leg Press', 'weights2', 'weights2', '4'],
                         ['2023-10-25', 'Leg Press', 'weights2', 'weights2', '5'],
                         ['2023-10-25', 'Bent Over Row', 'weights3', 'weights3', '3'],
                         ['2023-10-25', 'Bent Over Row', 'weights3', 'weights3', '4'],
                         ['2023-10-25', 'Bent Over Row', 'weights3', 'weights3', '5'],
                         ['2023-10-25', 'Barbell Curl', 'weights4', 'weights4', '3'],
                         ['2023-10-25', 'Barbell Curl', 'weights4', 'weights4', '4'],
                         ['2023-10-25', 'Barbell Curl', 'weights4', 'weights4', '5'],
                         ['2023-10-25', 'Pullups', 'weights5', 'weights5', '3'],
                         ['2023-10-25', 'Pullups', 'weights5', 'weights5', '4'],
                         ['2023-10-25', 'Pullups', 'weights5', 'weights5', '5']]
        self.assertEqual(list(actual_rows), expected_rows)

    def test_extract_weights_from_formula(self):
        formula = '=(40+8)*6*3'
        weights_plates, weights_equipment = extract_weights_from_formula(formula)
        self.assertEqual('40', weights_plates)
        self.assertEqual('8', weights_equipment)

    def test_extract_weights_from_formula_no_parentheses(self):
        formula = '=60*3*9'
        weights_plates, weights_equipment = extract_weights_from_formula(formula)
        self.assertEqual('60', weights_plates)
        self.assertEqual('0', weights_equipment)

    def test_extract_weights_from_formula_negative(self):
        formula = '=(90-28)*3*9'
        weights_plates, weights_equipment = extract_weights_from_formula(formula)
        self.assertEqual('-28', weights_plates)
        self.assertEqual('0', weights_equipment)

    def test_extract_weights_from_formula_no_operator(self):
        formula = '=90'
        weights_plates, weights_equipment = extract_weights_from_formula(formula)
        self.assertEqual('90', weights_plates)
        self.assertEqual('0', weights_equipment)

    def test_extract_weights_from_formula_when_none(self):
        formula = None
        weights = extract_weights_from_formula(formula)
        expected_weights = ('0', '0')
        self.assertEqual(weights, expected_weights)

    def test_extract_sets_and_reps_from_formula_reps_first(self):
        formula = '=(40+8)*6*3'
        sets = extract_sets_and_reps_from_formula(formula)
        expected_sets = ['6', '6', '6']
        self.assertEqual(sets, expected_sets)

    def test_extract_sets_and_reps_from_formula_sets_first(self):
        formula = '=(90-28)*3*9'
        sets = extract_sets_and_reps_from_formula(formula)
        expected_sets = ['9', '9', '9']
        self.assertEqual(sets, expected_sets)

    def test_extract_sets_and_reps_from_formula_parentheses(self):
        formula = '=(90-28)*(10+10+6)'
        sets = extract_sets_and_reps_from_formula(formula)
        expected_sets = ['10', '10', '6']
        self.assertEqual(expected_sets, sets)

