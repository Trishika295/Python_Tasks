import json
import os


class StudentManager:

    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self.load_students()

    # -----------------------------
    # Load students from JSON
    # -----------------------------
    def load_students(self):

        if not os.path.exists(self.filename):
            self.students = []
            self.save_students()
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, list):
                    self.students = data
                else:
                    self.students = []

        except (json.JSONDecodeError, OSError):
            self.students = []

    # -----------------------------
    # Save students to JSON
    # -----------------------------
    def save_students(self):

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                self.students,
                file,
                indent=4
            )

    # -----------------------------
    # Generate student ID
    # -----------------------------
    def generate_id(self):

        if not self.students:
            return 1

        return max(
            student["id"]
            for student in self.students
        ) + 1

    # -----------------------------
    # Validate student data
    # -----------------------------
    def validate_student(self, name, marks):

        if not name or not name.strip():
            raise ValueError(
                "Student name cannot be empty."
            )

        try:
            marks = float(marks)
        except (ValueError, TypeError):
            raise ValueError(
                "Marks must be a valid number."
            )

        if marks < 0 or marks > 100:
            raise ValueError(
                "Marks must be between 0 and 100."
            )

        return name.strip(), marks

    # -----------------------------
    # Add student
    # -----------------------------
    def add_student(self, name, marks):

        name, marks = self.validate_student(
            name,
            marks
        )

        student = {
            "id": self.generate_id(),
            "name": name,
            "marks": marks
        }

        self.students.append(student)

        self.save_students()

        return student

    # -----------------------------
    # Get all students
    # -----------------------------
    def get_students(self):

        return self.students

    # -----------------------------
    # Search students
    # -----------------------------
    def search_students(self, name):

        search_name = name.strip().lower()

        if not search_name:
            return self.students

        return [
            student
            for student in self.students
            if search_name in student["name"].lower()
        ]

    # -----------------------------
    # Sort students
    # -----------------------------
    def sort_students(self, order="desc"):

        if order == "asc":

            return sorted(
                self.students,
                key=lambda student: student["marks"]
            )

        return sorted(
            self.students,
            key=lambda student: student["marks"],
            reverse=True
        )

    # -----------------------------
    # Get highest score
    # -----------------------------
    def get_highest(self):

        if not self.students:
            return None

        return max(
            self.students,
            key=lambda student: student["marks"]
        )

    # -----------------------------
    # Get lowest score
    # -----------------------------
    def get_lowest(self):

        if not self.students:
            return None

        return min(
            self.students,
            key=lambda student: student["marks"]
        )

    # -----------------------------
    # Calculate statistics
    # -----------------------------
    def get_statistics(self):

        total_students = len(self.students)

        if total_students == 0:

            return {
                "total_students": 0,
                "highest": None,
                "lowest": None,
                "average": 0
            }

        total_marks = sum(
            student["marks"]
            for student in self.students
        )

        average = total_marks / total_students

        return {
            "total_students": total_students,
            "highest": self.get_highest(),
            "lowest": self.get_lowest(),
            "average": round(average, 2)
        }

    # -----------------------------
    # Delete student
    # -----------------------------
    def delete_student(self, student_id):

        try:
            student_id = int(student_id)
        except (ValueError, TypeError):
            return False

        original_length = len(self.students)

        self.students = [
            student
            for student in self.students
            if student["id"] != student_id
        ]

        if len(self.students) == original_length:
            return False

        self.save_students()

        return True


# ------------------------------------------------
# Command Line Interface
# ------------------------------------------------

def display_students(students):

    if not students:

        print("\nNo student records found.")

        return

    print("\n" + "=" * 60)

    print(
        f"{'ID':<8}"
        f"{'Name':<30}"
        f"{'Marks':<10}"
    )

    print("=" * 60)

    for student in students:

        print(
            f"{student['id']:<8}"
            f"{student['name']:<30}"
            f"{student['marks']:<10.2f}"
        )

    print("=" * 60)


def display_statistics(manager):

    statistics = manager.get_statistics()

    print("\n" + "=" * 50)

    print("STUDENT STATISTICS")

    print("=" * 50)

    print(
        f"Total Students : "
        f"{statistics['total_students']}"
    )

    if statistics["highest"]:

        print(
            f"Highest Score  : "
            f"{statistics['highest']['marks']:.2f} "
            f"({statistics['highest']['name']})"
        )

        print(
            f"Lowest Score   : "
            f"{statistics['lowest']['marks']:.2f} "
            f"({statistics['lowest']['name']})"
        )

        print(
            f"Average Score  : "
            f"{statistics['average']:.2f}"
        )

    else:

        print("Highest Score  : —")
        print("Lowest Score   : —")
        print("Average Score  : —")

    print("=" * 50)


def run_cli():

    manager = StudentManager()

    print("\n" + "=" * 60)
    print("       STUDENT RECORDS MANAGEMENT SYSTEM")
    print("=" * 60)

    while True:

        print("\n")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Sort Students")
        print("5. View Statistics")
        print("6. Delete Student")
        print("7. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # -------------------------
        # Add
        # -------------------------

        if choice == "1":

            print("\n--- ADD STUDENT ---")

            name = input(
                "Enter student name: "
            ).strip()

            marks = input(
                "Enter marks (0-100): "
            ).strip()

            try:

                student = manager.add_student(
                    name,
                    marks
                )

                print(
                    f"\nStudent added successfully!"
                )

                print(
                    f"ID: {student['id']}"
                )

                print(
                    f"Name: {student['name']}"
                )

                print(
                    f"Marks: {student['marks']:.2f}"
                )

            except ValueError as error:

                print(
                    f"\nError: {error}"
                )

        # -------------------------
        # View
        # -------------------------

        elif choice == "2":

            print("\n--- ALL STUDENTS ---")

            display_students(
                manager.get_students()
            )

        # -------------------------
        # Search
        # -------------------------

        elif choice == "3":

            print("\n--- SEARCH STUDENT ---")

            name = input(
                "Enter student name: "
            ).strip()

            results = manager.search_students(
                name
            )

            display_students(results)

        # -------------------------
        # Sort
        # -------------------------

        elif choice == "4":

            print("\n--- SORT STUDENTS ---")

            print("1. Highest to Lowest")
            print("2. Lowest to Highest")

            sort_choice = input(
                "Enter choice: "
            ).strip()

            if sort_choice == "1":

                students = manager.sort_students(
                    "desc"
                )

                display_students(students)

            elif sort_choice == "2":

                students = manager.sort_students(
                    "asc"
                )

                display_students(students)

            else:

                print("\nInvalid sorting choice.")

        # -------------------------
        # Statistics
        # -------------------------

        elif choice == "5":

            display_statistics(manager)

        # -------------------------
        # Delete
        # -------------------------

        elif choice == "6":

            print("\n--- DELETE STUDENT ---")

            student_id = input(
                "Enter student ID: "
            ).strip()

            deleted = manager.delete_student(
                student_id
            )

            if deleted:

                print(
                    "\nStudent deleted successfully."
                )

            else:

                print(
                    "\nStudent ID not found."
                )

        # -------------------------
        # Exit
        # -------------------------

        elif choice == "7":

            print(
                "\nThank you for using "
                "Student Records Management System!"
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-7."
            )


if __name__ == "__main__":

    run_cli()