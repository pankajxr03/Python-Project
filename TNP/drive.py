class PlacementDrive:
    def __init__(self, drive_id, company, eligible_branch, date, applicants=None):
        self.drive_id = drive_id
        self.company = company
        self.eligible_branch = eligible_branch
        self.date = date
        self.applicants = applicants if applicants is not None else []

    def to_dict(self):
        return {
            "drive_id": self.drive_id,
            "company": self.company,
            "eligible_branch": self.eligible_branch,
            "date": self.date,
            "applicants": self.applicants
        }
