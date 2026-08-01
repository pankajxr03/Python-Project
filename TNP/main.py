from utils import (
    load_students_json, save_students_json, load_drives_json, save_drives_json,
    import_students_from_csv, export_students_to_csv,
    import_drives_from_csv, export_drives_to_csv
)
from student import Student
from drive import PlacementDrive


def add_student(students):
    id = input("Student ID: ").strip()
    name = input("Name: ").strip()
    branch = input("Branch: ").strip()
    contact = input("Contact: ").strip()
    students[id] = Student(id, name, branch, contact)
    save_students_json(students)
    print("✅ Student added.\n")


def add_drive(drives):
    drive_id = input("Drive ID: ").strip()
    company = input("Company Name: ").strip()
    eligible_branch = input("Eligible Branch: ").strip()
    date = input("Drive Date (YYYY-MM-DD): ").strip()
    drives[drive_id] = PlacementDrive(drive_id, company, eligible_branch, date)
    save_drives_json(drives)
    print("✅ Drive added.\n")


def apply_for_drive(students, drives):
    student_id = input("Student ID: ").strip()
    drive_id = input("Drive ID: ").strip()
    student = students.get(student_id)
    drive = drives.get(drive_id)

    if student and drive:
        if student.placement_status == "Not Placed" and student.branch == drive.eligible_branch:
            if student_id not in drive.applicants:
                drive.applicants.append(student_id)
                save_drives_json(drives)
                print(f"✅ {student.name} successfully applied to {drive.company}!\n")
            else:
                print("⚠️ Already applied.\n")
        elif student.placement_status != "Not Placed":
            print("⚠️ Already placed, cannot apply.\n")
        else:
            print("⚠️ Not eligible for this drive.\n")
    else:
        print("❌ Invalid Student ID or Drive ID.\n")


def mark_student_as_placed(students):
    student_id = input("Student ID: ").strip()
    student = students.get(student_id)
    if student:
        student.placement_status = "Placed"
        save_students_json(students)
        print("✅ Marked as placed.\n")
    else:
        print("❌ Student not found.\n")


def view_placed_students(students):
    print("\n🎓 Placed Students:")
    placed = [s for s in students.values() if s.placement_status == "Placed"]
    if placed:
        for student in placed:
            print(f"{student.id} - {student.name} ({student.branch})")
    else:
        print("No students placed yet.")
    print()


def view_applicants_for_drive(students, drives):
    drive_id = input("Enter Drive ID: ").strip()
    drive = drives.get(drive_id)
    if not drive:
        print("❌ Drive not found.\n")
        return

    if not drive.applicants:
        print(f"ℹ️ No students have applied for {drive.company} yet.\n")
        return

    print(f"\n📋 Applicants for {drive.company} ({drive.drive_id}):")
    for sid in drive.applicants:
        student = students.get(sid)
        if student:
            print(f"{student.id} - {student.name} ({student.branch}) - {student.placement_status}")
        else:
            print(f"{sid} - [Student record missing]")
    print()


def view_all_drives(drives):
    print("\n🏢 All Placement Drives:")
    if not drives:
        print("No drives available.\n")
        return
    for drive in drives.values():
        print(f"{drive.drive_id} - {drive.company} | Eligible: {drive.eligible_branch} | Date: {drive.date} | Applicants: {len(drive.applicants)}")
    print()


def menu():
    students = load_students_json()
    drives = load_drives_json()

    while True:
        print("=== Placement Management System ===")
        print("1. Add Student")
        print("2. Add Drive")
        print("3. Apply for Drive")
        print("4. Mark Student as Placed")
        print("5. View Placed Students")
        print("6. View Applicants for Drive")
        print("7. View All Drives (Summary)")
        print("8. Import Students from CSV")
        print("9. Export Students to CSV")
        print("10. Import Drives from CSV")
        print("11. Export Drives to CSV")
        print("12. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            add_drive(drives)
        elif choice == "3":
            apply_for_drive(students, drives)
        elif choice == "4":
            mark_student_as_placed(students)
        elif choice == "5":
            view_placed_students(students)
        elif choice == "6":
            view_applicants_for_drive(students, drives)
        elif choice == "7":
            view_all_drives(drives)
        elif choice == "8":
            filename = input("Enter student CSV filename: ").strip()
            import_students_from_csv(filename, students)
        elif choice == "9":
            filename = input("Export to student CSV filename: ").strip()
            export_students_to_csv(filename, students)
        elif choice == "10":
            filename = input("Enter drives CSV filename: ").strip()
            import_drives_from_csv(filename, drives)
        elif choice == "11":
            filename = input("Export to drive CSV filename: ").strip()
            export_drives_to_csv(filename, drives)
        elif choice == "12":
            print("👋 Exiting Placement Management System...")
            break
        else:
            print("❌ Invalid choice.\n")


if __name__ == "__main__":
    menu()
