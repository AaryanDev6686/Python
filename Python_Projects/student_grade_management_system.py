#Initialising Dictionary 
student_grades = { }

#Add a new student
def add_student(name, grade):
    student_grades[name] = grade
    print(f"Added {name} with {grade}")

#Update a student
def update_student(name, grade):
    if name in student_grades:
        student_grades [name]= grade
        print(f"{name} has been updated with a {grade}")
    else:
        print(f"{name} is not found!")

#Delete a student
def delete_student(name):
    if name in student_grades:
        del student_grades[name]
        print(f"{name} has been deleted successfully")
    else:
        print(f"{name} is not found!")

#View all students
def display_all_students():
    if student_grades:
        for name, grade in student_grades.items():
            print(f"{name} : {grade}")
    
    else:
        print("NO student found/added!")

def main():
    while True:
        print("\nStudent Grades Management System")
        print("1. Add a Student")
        print("2. Update a Student")
        print("3. View All Students")
        print("4. Delete a Student")

        choice = int(input("Enter you choice: "))
        if choice == 1:
            add_student()
        
        elif choice == 2:
            update_student()
        
        elif choice == 3:
            display_all_students()
        
        elif choice == 4:
            delete_student()
        else:
            print("No such options!")