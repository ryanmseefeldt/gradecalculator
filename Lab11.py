import os
import matplotlib.pyplot as plt

def read_students(file_path):
    students = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Assuming format is "123Student Name" where 123 is the student ID
            if len(line) >= 3:
                student_id = line[:3]
                name = line[3:].strip()
                students[student_id] = name
    return students

def read_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Check if there are enough characters for the format
            if len(line) >= 6:  # Minimum for a 5-digit ID and a single character name
                # Handle Quiz 8 with 4-digit ID specially
                if "Quiz 8" in line:
                    # Assuming format for Quiz 8: "1234Quiz 8,25"
                    assignment_id_length = 4
                else:
                    # Assuming format: "12345Assignment Name,25"
                    assignment_id_length = 5

                assignment_id = line[:assignment_id_length]
                rest = line[assignment_id_length:]

                # Find where the points value starts (after the last comma)
                last_comma = rest.rfind(',')
                if last_comma != -1:
                    name = rest[:last_comma].strip()
                    points_str = rest[last_comma + 1:].strip()
                    try:
                        points = float(points_str)
                        assignments[assignment_id] = (name, points)
                    except ValueError:
                        print(f"Warning: Invalid points value in line: {line}")
    return assignments

def read_submissions(submissions_dir):
    submissions = []
    for filename in os.listdir(submissions_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(submissions_dir, filename)
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Assuming format: "123|12345|75" for student_id|assignment_id|percentage
                    parts = line.split('|')
                    if len(parts) == 3:
                        student_id, assignment_id, percentage = parts
                        try:
                            submissions.append((student_id, assignment_id, float(percentage)))
                        except ValueError:
                            print(f"Warning: Invalid percentage in submission: {line}")
    return submissions

def calculate_student_grade(student_name, students, assignments, submissions):
    # Find student_id by name
    student_id = None
    for sid, name in students.items():
        if name.lower() == student_name.lower():
            student_id = sid
            break

    if student_id is None:
        print("Student not found")
        return

    total_points_earned = 0
    total_points_possible = sum(points for _, points in assignments.values())

    if total_points_possible == 0:
        print("No valid assignments found")
        return

    # Calculate points earned for the student
    for submission in submissions:
        if submission[0] == student_id:
            assignment_id = submission[1]
            percentage = submission[2]
            if assignment_id in assignments:
                points = assignments[assignment_id][1]
                total_points_earned += (percentage / 100) * points

    grade_percentage = (total_points_earned / total_points_possible) * 100
    print(f"{round(grade_percentage)}%")

def calculate_assignment_stats(assignment_name, assignments, submissions):
    # Find assignment_id by name
    assignment_id = None
    for aid, (name, _) in assignments.items():
        if name.lower() == assignment_name.lower():
            assignment_id = aid
            break
    if assignment_id is None:
        print("Assignment not found")
        return
    percentages = [s[2] for s in submissions if s[1] == assignment_id]
    if not percentages:
        print("No submissions found for this assignment")
        return

    print(f"Min: {round(min(percentages))}%")
    print(f"Avg: {round(sum(percentages) / len(percentages))}%")
    print(f"Max: {round(max(percentages))}%")

def plot_assignment_histogram(assignment_name, assignments, submissions):
    # Find assignment_id by name
    assignment_id = None
    for aid, (name, _) in assignments.items():
        if name.lower() == assignment_name.lower():
            assignment_id = aid
            break

    if assignment_id is None:
        print("Assignment not found")
        return

    percentages = [s[2] for s in submissions if s[1] == assignment_id]
    if not percentages:
        print("No submissions found for this assignment")
        return

    plt.hist(percentages, bins=[0, 25, 50, 75, 100], edgecolor='black')
    plt.title(f"Histogram of {assignment_name} Scores")
    plt.xlabel("Percentage")
    plt.ylabel("Number of Students")
    plt.show()

def main():
    # File paths
    students_file = 'data/students.txt'
    assignments_file = 'data/assignments.txt'
    submissions_dir = 'data/submissions'

    # Read data and print debug info
    students = read_students(students_file)
    assignments = read_assignments(assignments_file)
    submissions = read_submissions(submissions_dir)

    # Debug print statements
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    selection = input("Enter your selection: ")

    if selection == '1':
        student_name = input("What is the student's name: ")
        calculate_student_grade(student_name, students, assignments, submissions)
    elif selection == '2':
        assignment_name = input("What is the assignment name: ")
        calculate_assignment_stats(assignment_name, assignments, submissions)
    elif selection == '3':
        assignment_name = input("What is the assignment name: ")
        plot_assignment_histogram(assignment_name, assignments, submissions)

if __name__ == "__main__":
    main()