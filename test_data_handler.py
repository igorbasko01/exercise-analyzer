import unittest

from data_handler import extract_exercise_names


class DataHandlerTests(unittest.TestCase):
    def test_extract_exercise_names(self):
        exercise_names = extract_exercise_names(['Date', 'Chest', 'Squat', 'Row', 'Biceps W', 'Pullups', 'col1', 'col2'])
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
