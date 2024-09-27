from openpyxl import load_workbook

from data_handler import extract_exercise_names

original_exercise_names = ['Chest', 'Squat', 'Row', 'Biceps W', 'Pullups']
new_exercise_names = ['Bench Press', 'Leg Press', 'Bent Over Row', 'Barbell Curl', 'Pullups']

wb = load_workbook('Exercise.xlsx', data_only=False)

ws = wb['Combined']

# Extract the first row, converts tuple to list, the next is used to actually extract the row from the generator.
first_row = list(map(lambda x: x.value, list(next(ws.iter_rows(min_row=1, max_row=1)))))


exercise_names = extract_exercise_names(first_row, original_exercise_names)
print('Exercise names:', exercise_names)

for row in ws.iter_rows():
    row_data = []
    for cell in row:
        if cell.value is not None:
            row_data.append(cell.value)
        else:
            row_data.append(None)
    print(row_data)
