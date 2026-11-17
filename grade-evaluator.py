import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the csv file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Processes assignment records, validates constraints, calculates GPA,
    determines pass/fail status, and identifies resubmission candidates.
    """
    print("\n--- Processing Grades ---")

    # TODO: a) Check if all scores are percentage based (0-100)
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"Error: Score for '{item['assignment']}' must be between 0 and 100.")
            return

    # TODO: b) Validate total weights (Total=100, Summative=40, Formative=60)
    summative_weight = sum(item['weight'] for item in data if item['group'] == 'Summative')
    formative_weight = sum(item['weight'] for item in data if item['group'] == 'Formative')
    total_weight = summative_weight + formative_weight

    if total_weight != 100 or summative_weight != 40 or formative_weight != 60:
        print("Error: Invalid weight configuration. Summative must equal 40, Formative 60, and Total 100.")
        return

    # TODO: c) Calculate the Final Grade and GPA
    summative_score = sum((item['score'] * item['weight']) / 100 for item in data if item['group'] == 'Summative')
    formative_score = sum((item['score'] * item['weight']) / 100 for item in data if item['group'] == 'Formative')

    # Convert category scores to percentages out of their respective maximum category weights
    summative_pct = (summative_score / 40) * 100
    formative_pct = (formative_score / 60) * 100

    total_grade = summative_score + formative_score
    gpa = (total_grade / 100) * 5.0

    print(f"Summative Score: {summative_pct:.2f}%")
    print(f"Formative Score: {formative_pct:.2f}%")
    print(f"Total Grade: {total_grade:.2f}%")
    print(f"GPA: {gpa:.2f}")

    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    # TODO: f) Print the final decision (PASSED / FAILED)
    if summative_pct >= 50 and formative_pct >= 50:
        status = "PASSED"
    else:
        status = "FAILED"
    print(f"Final Decision: {status}")

    # TODO: e) Check for failed formative assignments (< 50%) and highest weight resubmission
    failed_formatives = [item for item in data if item['group'] == 'Formative' and item['score'] < 50]

    if failed_formatives:
        max_weight = max(item['weight'] for item in failed_formatives)
        eligible = [item['assignment'] for item in failed_formatives if item['weight'] == max_weight]
        print("Eligible for Resubmission:", ", ".join(eligible))
    else:
        print("Eligible for Resubmission: None")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
