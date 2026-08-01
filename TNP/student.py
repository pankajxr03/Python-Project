class Student:
    def __init__(self, id, name, branch, contact, placement_status="Not Placed"):
        self.id = id
        self.name = name
        self.branch = branch
        self.contact = contact
        self.placement_status = placement_status

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "branch": self.branch,
            "contact": self.contact,
            "placement_status": self.placement_status
        }
