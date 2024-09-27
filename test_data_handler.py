import datetime
import unittest

from data_handler import extract_exercise_names, explode_exercises


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
        def sample_weights_extractor(formula: str) -> str:
            return formula

        def sample_reps_extractor(formula: str) -> str:
            return '3'

        header_row = ['Date', 'Chest', 'Squat', 'Row', 'Biceps W', 'Pullups']
        alternative_exercise_names = ['Bench Press', 'Leg Press', 'Bent Over Row', 'Barbell Curl', 'Pullups']
        input_rows = [[datetime.datetime(2023, 10, 25), 'weights1', 'weights2', 'weights3', 'weights4', 'weights5']]
        actual_rows = explode_exercises(input_rows, header_row, sample_weights_extractor, sample_reps_extractor,
                                        alternative_exercise_names)
        expected_rows = [['2023-10-25', 'Bench Press', 'weights1', '3'],
                         ['2023-10-25', 'Leg Press', 'weights2', '3'],
                         ['2023-10-25', 'Bent Over Row', 'weights3', '3'],
                         ['2023-10-25', 'Barbell Curl', 'weights4', '3'],
                         ['2023-10-25', 'Pullups', 'weights5', '3']]
        self.assertEqual(list(actual_rows), expected_rows)

    def test_explode_exercises_skip_row_starts_with_not_a_date(self):
        def sample_weights_extractor(formula: str) -> str:
            return formula

        def sample_reps_extractor(formula: str) -> str:
            return '3'

        header_row = ['Date', 'Chest', 'Squat', 'Row', 'Biceps W', 'Pullups']
        alternative_exercise_names = ['Bench Press', 'Leg Press', 'Bent Over Row', 'Barbell Curl', 'Pullups']
        input_rows = [[None, 'weights1', 'weights2', 'weights3', 'weights4', 'weights5']]
        actual_rows = explode_exercises(input_rows, header_row, sample_weights_extractor, sample_reps_extractor,
                                        alternative_exercise_names)
        expected_rows = []
        self.assertEqual(list(actual_rows), expected_rows)
