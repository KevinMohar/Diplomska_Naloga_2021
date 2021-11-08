class Aisle():
    id: int
    name: str

    def __init__(self, id, name):
        self.id = int(id)
        self.name = name

    def __repr__(self):
        return f"Aisle {self.id}: {self.name}\n"


class Department():
    id: int
    name: str

    def __init__(self, id, name):
        self.id = int(id)
        self.name = name

    def __repr__(self):
        return f"Department {self.id}: {self.name}\n"


class Product():
    id: int
    name: str
    aisle: Aisle
    department: Department

    def __init__(self, id, name, aisle, department):
        self.id = int(id)
        self.name = name
        self.aisle = aisle
        self.department = department

    def __repr__(self):
        return f"Product {self.id}:\n    Name: {self.name}\n    Aisle: {self.aisle.name}(id:{self.aisle.id})\n    Department: {self.department.name}(id:{self.department.id})\n"
