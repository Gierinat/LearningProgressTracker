import re

acceptable_commands = ['exit', 'add students', 'back', 'list', 'add points']
ERROR_MSG = ("No input", "Unknown command!", "Incorrect credentials", "This email is already taken")
INFO_MSG = ("Bye!", "Enter 'exit' to exit the program.", "Enter student credentials or 'back' to return",
            "No students found", "Enter an id and points or 'back' to return:")
student_dict = {}
student_points = {}


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
        student_points[id_s] = {'P': 0, 'DSA': 0, 'DB': 0, 'F': 0}
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
        for key in student_dict.keys():
            print(key)


def add_points():
    entry = ""
    while entry != 'back':
        entry = input()
        if entry == 'back':
            break


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
        elif command == 'back':
            print(INFO_MSG[1])
        elif command == 'exit':
            print(INFO_MSG[0])


if __name__ == "__main__":
    main()
