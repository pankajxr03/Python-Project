import json
import csv
from student import Student
from drive import PlacementDrive

# -------------------- JSON HANDLING --------------------
def load_students_json(filename="students.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return {s["id"]: Student(**s) for s in data}
    except FileNotFoundError:
        return {}

def save_students_json(students, filename="students.json"):
    with open(filename, "w") as f:
        json.dump([s.to_dict() for s in students.values()], f, indent=2)

def load_drives_json(filename="drives.json"):
    try:
        with open(filename, "r") as f:
            drives_data = json.load(f)
            drives = {}
            for d in drives_data:
                drive = PlacementDrive(
                    d["drive_id"], d["company"], d["eligible_branch"], d["date"],
                    applicants=d.get("applicants", [])
                )
                drives[drive.drive_id] = drive
            return drives
    except FileNotFoundError:
        return {}

def save_drives_json(drives, filename="drives.json"):
    with open(filename, "w") as f:
        json.dump([d.to_dict() for d in drives.values()], f, indent=2)

# -------------------- CSV HANDLING --------------------
def import_students_from_csv(filename, students):
    if not filename.lower().endswith(".csv"):
        filename += ".csv"
    try:
        with open(filename, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student = Student(
                    id=row['id'],
                    name=row['name'],
                    branch=row['branch'],
                    contact=row['contact'],
                    placement_status=row.get('placement_status', 'Not Placed')
                )
                students[student.id] = student
        save_students_json(students)
        print(f"✅ Imported {len(students)} students from {filename}.")
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")

def export_students_to_csv(filename, students):
    if not filename.lower().endswith(".csv"):
        filename += ".csv"
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["id", "name", "branch", "contact", "placement_status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for student in students.values():
            writer.writerow(student.to_dict())
    print(f"✅ Exported students to {filename}.")

def import_drives_from_csv(filename, drives):
    if not filename.lower().endswith(".csv"):
        filename += ".csv"
    try:
        with open(filename, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                drive = PlacementDrive(
                    drive_id=row['drive_id'],
                    company=row['company'],
                    eligible_branch=row['eligible_branch'],
                    date=row['date']
                )
                drives[drive.drive_id] = drive
        save_drives_json(drives)
        print(f"✅ Imported {len(drives)} drives from {filename}.")
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")

def export_drives_to_csv(filename, drives):
    if not filename.lower().endswith(".csv"):
        filename += ".csv"
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["drive_id", "company", "eligible_branch", "date", "applicants"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for drive in drives.values():
            drive_data = drive.to_dict()
            drive_data["applicants"] = ",".join(drive_data["applicants"])
            writer.writerow(drive_data)
    print(f"✅ Exported drives to {filename}.")
