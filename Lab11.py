import os
import matplotlib.pyplot as plt

def read_students(file_path):
    students = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, student_id = line.strip().split(',')
            students[name] = student_id
    return students

def read_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, points, assignment_id = line.strip().split(',')
            assignments[name] = {'points': int(points), 'id': assignment_id}
    return assignments

def read_submissions(dir_path):
    submissions = {}
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'r') as file:
            for line in file:
                student_id, assignment_id, percent = line.strip().split(',')
                submissions[(student_id, assignment_id)] = float(percent)
    return submissions

def calculate_student_grade(student_name, students, assignments, submissions):
    if student_name not in students:
        print("Student not found")
        return
    student_id = students[student_name]
    total_points = sum(assignment['points'] for assignment in assignments.values())
    earned_points = sum(
        submissions[(student_id, assignment['id'])] * assignment['points'] / 100
        for assignment in assignments.values()
    )
    grade_percentage = round((earned_points / total_points) * 100)
    print(f"{grade_percentage}%")

def assignment_statistics(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        print("Assignment not found")
        return
    assignment_id = assignments[assignment_name]['id']
    percents = [
        submissions[(student_id, assignment_id)]
        for (student_id, a_id) in submissions
        if a_id == assignment_id
    ]
    min_score = round(min(percents))
    avg_score = round(sum(percents) / len(percents))
    max_score = round(max(percents))
    print(f"Min: {min_score}%\nAvg: {avg_score}%\nMax: {max_score}%")

def assignment_graph(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        print("Assignment not found")
        return
    assignment_id = assignments[assignment_name]['id']
    scores = [
        submissions[(student_id, assignment_id)]
        for (student_id, a_id) in submissions
        if a_id == assignment_id
    ]
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Scores Distribution for {assignment_name}")
    plt.xlabel("Percentage Scores")
    plt.ylabel("Number of Students")
    plt.show()

def main():
    students = read_students('data/students.txt')
    assignments = read_assignments('data/assignments.txt')
    submissions = read_submissions('data/submissions')

    print("1. Student grade\n2. Assignment statistics\n3. Assignment graph")
    selection = input("Enter your selection: ")

    if selection == '1':
        student_name = input("What is the student's name: ")
        calculate_student_grade(student_name, students, assignments, submissions)
    elif selection == '2':
        assignment_name = input("What is the assignment name: ")
        assignment_statistics(assignment_name, assignments, submissions)
    elif selection == '3':
        assignment_name = input("What is the assignment name: ")
        assignment_graph(assignment_name, assignments, submissions)

if __name__ == "__main__":
    main()
