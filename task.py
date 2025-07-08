import re

acceptable_commands = ['exit', 'add students', 'back', 'list', 'add points', 'find', 'statistics']
ERROR_MSG = ("No input", "Unknown command!", "Incorrect credentials", "This email is already taken",
             "Incorrect points format.", "No student is found for id=%s")
INFO_MSG = ("Bye!", "Enter 'exit' to exit the program.", "Enter student credentials or 'back' to return",
            "No students found", "Enter an id and points or 'back' to return:", "Points updated.",
            "Enter an id or 'back' to return", "Type the name of a course to see details or 'back' to quit")
student_dict = {}
student_points = {}
course_stats = {'Python': {'max': 600, 'users': set(), 'submissions': 0},
                'DSA': {'max': 400, 'users': set(), 'submissions': 0},
                'Databases': {'max': 480, 'users': set(), 'submissions': 0},
                'Flask': {'max': 550, 'users': set(), 'submissions': 0}}


def validate_command():
    while True:
        command = input().lower().strip()
        if command == '':
            print(ERROR_MSG[0])
        elif command not in acceptable_commands:
            print(ERROR_MSG[1])
        else:
            return command


def save_student(email, first_name, last_name):
    id_s = abs(hash(email)) % (10**5 + 7)
    if id_s in student_dict:
        print(ERROR_MSG[3])
        return False
    else:
        details = {'email': email, 'f_name': first_name, 'l_name': last_name}
        student_dict[id_s] = details
        student_points[id_s] = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
        return True


def add_student():
    entry = ""
    total_entries = 0
    while entry != 'back':
        entry = input()
        if entry == 'back':
            return total_entries

        student = entry.split()
        if len(student) < 3:
            print(ERROR_MSG[2])
            continue

        email = student.pop()
        first_name = student.pop(0)
        last_name = " ".join(student)

        if not validate_name(first_name, "first name"):
            continue
        if not validate_name(last_name, "last name"):
            continue
        if not validate_email(email):
            continue
        if not save_student(email, first_name, last_name):
            continue

        print("The student has been added.")
        total_entries += 1
        print(student_dict)


def validate_name(validate_string, name):
    if re.search("[^A-Za-z- ']", validate_string) or re.search("([-'])$|^([-'])|''|--|-'|'-", validate_string)\
            or len(validate_string) < 2:
        print("Incorrect", name)
        return False
    else:
        return True


def validate_email(validate_string):
    if re.match("[^@\r\n\t\f\v ]*@[^@\r\n\t\f\v ]*\.[a-z0-9]*", validate_string):
        return True
    else:
        print("Incorrect email")
        return False


def list_students():
    if len(student_dict) == 0:
        print(INFO_MSG[3])
    else:
        print("Students:")
        for key in student_dict.keys():
            print(key)


def check_student_exist(student):
    if student in student_dict.keys():
        return True
    else:
        print(ERROR_MSG[5] % student)
        return False


def validate_points(points):
    if len(points) != 4:
        print(ERROR_MSG[4])
        return False

    try:
        points = [int(x) for x in points]
        val = sum(points) == sum(abs(x) for x in points)
    except (ValueError, TypeError):
        print(ERROR_MSG[4])
        return False

    if val:
        return points
    else:
        print(ERROR_MSG[4])
        return False


def save_points(student, points):
    student_points[student]['Python'] += points[0]
    if points[0]:
        course_stats['Python']['users'].add(student)
        course_stats['Python']['submissions'] += 1

    student_points[student]['DSA'] += points[1]
    if points[1]:
        course_stats['DSA']['users'].add(student)
        course_stats['DSA']['submissions'] += 1

    student_points[student]['Databases'] += points[2]
    if points[2]:
        course_stats['Databases']['users'].add(student)
        course_stats['Databases']['submissions'] += 1

    student_points[student]['Flask'] += points[3]
    if points[3]:
        course_stats['Flask']['users'].add(student)
        course_stats['Flask']['submissions'] += 1


def add_points():
    entry = ""
    while entry != 'back':
        entry = input()
        if entry == 'back':
            break

        student_and_points = entry.split()
        student = student_and_points.pop(0)
        try:
            student = int(student)
        except ValueError:
            print(ERROR_MSG[5] % student)
        if not check_student_exist(student):
            continue
        points = validate_points(student_and_points)
        if not points:
            continue

        save_points(student, points)
        print(INFO_MSG[5])


def display_student(student):
    output = ''
    for key, val in student_points[student].items():
        output += f"{key}={val}; "
    # Remove the last semicolon and space
    output = output.rstrip('; ')

    print(student, "points: ", output)


def find():
    entry = ""
    while entry != 'back':
        entry = input()
        if entry == 'back':
            break

        try:
            student = int(entry)
            if student in student_dict:
                display_student(student)
            else:
                print(ERROR_MSG[5] % entry)
        except (TypeError, ValueError):
            print(ERROR_MSG[5] % entry)
            continue


def calculate_popularity():
    # Count users
    counts = {}
    for course in course_stats:
        count = len(course_stats[course]['users'])
        counts.setdefault(count, []).append(course)

    if sum(len(u['users']) for u in course_stats.values()):
        # Sort by key descending
        sorted_keys = sorted(counts.keys(), reverse=True)

        # First and last positions
        m_popular = counts[sorted_keys[0]]  # values for highest key
        l_popular = counts[sorted_keys[-1]]  # values for lowest key
        return m_popular, l_popular
    else:
        return 'n/a', 'n/a'


def calculate_activity():
    # Count submissions
    counts = {}
    for course in course_stats:
        count = course_stats[course]['submissions']
        counts.setdefault(count, []).append(course)

    if sum(c['submissions'] for c in course_stats.values()):
        # Sort by key descending
        sorted_keys = sorted(counts.keys(), reverse=True)

        # First and last positions
        h_activity = counts[sorted_keys[0]]  # values for highest key
        l_activity = counts[sorted_keys[-1]]  # values for lowest key
        return h_activity, l_activity
    else:
        return 'n/a', 'n/a'


def display_stats():
    print(INFO_MSG[7])
    m_popular, l_popular = calculate_popularity()
    h_activity, l_activity = calculate_activity()
    print("Most popular:", ", ".join(m_popular))
    print("Least popular:", ", ".join(l_popular))
    print("Highest activity:", ", ".join(h_activity))
    print("Lowest activity:", ", ".join(l_activity))


def main():
    print("Learning progress tracker")
    command = ''
    while command != 'exit':
        command = validate_command()
        if command == 'add students':
            print(INFO_MSG[2])
            total_entries = add_student()
            print(f"Total {total_entries} students have been added.")
        elif command == 'list':
            list_students()
        elif command == 'add points':
            print(INFO_MSG[4])
            add_points()
        elif command == 'find':
            print(INFO_MSG[6])
            find()
        elif command == 'statistics':
            display_stats()
        elif command == 'back':
            print(INFO_MSG[1])
        elif command == 'exit':
            print(INFO_MSG[0])


if __name__ == "__main__":
    main()
