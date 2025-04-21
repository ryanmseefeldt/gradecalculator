import os
import matplotlib.pyplot as plt

# Function to read students.txt and return a dictionary of student_id: name
def read_students(file_path):
    students = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                student_id, name = parts
                students[student_id] = name
    return students

# Function to read assignments.txt and return a dictionary of assignment_id: (name, points)
def read_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3:
                assignment_id, name, points = parts
                assignments[assignment_id] = (name, float(points))
    return assignments

# Function to read all submission files and return a list of (student_id, assignment_id, percentage)
def read_submissions(submissions_dir):
    submissions = []
    for filename in os.listdir(submissions_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(submissions_dir, filename), 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        student_id, assignment_id, percentage = parts
                        submissions.append((student_id, assignment_id, float(percentage)))
    return submissions

# Function to calculate a student's total grade as a percentage
def calculate_student_grade(student_name, students, assignments, submissions):
    # Find student_id by name
    student_id = None
    for sid, name in students.items():
        if name.lower() == student_name.lower():
            student_id = sid
            break
    if not student_id:
        print("Student not found")
        return

    total_points_earned = 0
    total_points_possible = sum(points for _, points in assignments.values())

    # Calculate points earned for the student
    for submission in submissions:
        if submission[0] == student_id:
            assignment_id = submission[1]
            percentage = submission[2]
            if assignment_id in assignments:
                points = assignments[assignment_id][1]
                total_points_earned += (percentage / 100) * points

    # Calculate and print grade as a percentage
    grade_percentage = (total_points_earned / total_points_possible) * 100
    print(f"{round(grade_percentage)}%")

# Function to calculate assignment statistics (min, avg, max percentages)
def calculate_assignment_stats(assignment_name, assignments, submissions):
    # Find assignment_id by name
    assignment_id = None
    for aid, (name, _) in assignments.items():
        if name.lower() == assignment_name.lower():
            assignment_id = aid
            break
    if not assignment_id:
        print("Assignment not found")
        return

    # Collect all percentages for this assignment
    percentages = [s[2] for s in submissions if s[1] == assignment_id]
    if not percentages:
        print("Assignment not found")
        return

    # Calculate and print statistics
    print(f"Min: {round(min(percentages))}%")
    print(f"Avg: {round(sum(percentages) / len(percentages))}%")
    print(f"Max: {round(max(percentages))}%")

# Function to generate a histogram of assignment scores
def plot_assignment_histogram(assignment_name, assignments, submissions):
    # Find assignment_id by name
    assignment_id = None
    for aid, (name, _) in assignments.items():
        if name.lower() == assignment_name.lower():
            assignment_id = aid
            break
    if not assignment_id:
        print("Assignment not found")
        return

    # Collect all percentages for this assignment
    percentages = [s[2] for s in submissions if s[1] == assignment_id]
    if not percentages:
        print("Assignment not found")
        return

    # Plot histogram
    plt.hist(percentages, bins=[0, 25, 50, 75, 100], edgecolor='black')
    plt.title(f"Histogram of {assignment_name} Scores")
    plt.xlabel("Percentage")
    plt.ylabel("Number of Students")
    plt.show()

# Main program
def main():
    # File paths
    students_file = 'data/students.txt'
    assignments_file = 'data/assignments.txt'
    submissions_dir = 'data/submissions'

    # Read data
    students = read_students(students_file)
    assignments = read_assignments(assignments_file)
    submissions = read_submissions(submissions_dir)

    # Print menu
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