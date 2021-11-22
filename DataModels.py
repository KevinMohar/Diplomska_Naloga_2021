class Aisle():
    '''
    Aisle data model
    '''
    id: int
    name: str

    def __init__(self, id, name):
        self.id = int(id)
        self.name = name

    def __repr__(self):
        return f"Aisle {self.id}: {self.name}\n"


class Department():
    '''
    Department data model
    '''
    id: int
    name: str

    def __init__(self, id, name):
        self.id = int(id)
        self.name = name

    def __repr__(self):
        return f"Department {self.id}: {self.name}\n"


class Product():
    '''
    Product data model
    '''
    id: int
    name: str
    aisle: Aisle
    department: Department

    def __init__(self, id: int, name: str, aisle: Aisle, department: Department):
        self.id = id
        self.name = name
        self.aisle = aisle
        self.department = department

    def __repr__(self):
        return f"Product {self.id}:\n    Name: {self.name}\n    Aisle: {self.aisle.name}(id:{self.aisle.id})\n    Department: {self.department.name}(id:{self.department.id})\n"


class Order():
    '''
    Order data model
    '''

    id: int
    user_id: int
    eval_set: str
    order_number: int
    order_dow: int
    order_hour_of_day: int
    days_since_prior_order: int
    produc_list: list

    def __init__(self, id: int, user_id: int, eval_set: str, order_number: int, order_dow: int, order_hour_of_day: int, days_since_prior_order: int):
        self.id = id
        self.user_id = user_id
        self.eval_set = eval_set
        self.order_number = order_number
        self.order_dow = order_dow
        self.order_hour_of_day = order_hour_of_day
        self.days_since_prior_order = days_since_prior_order

    def __repr__(self):
        return f"Order {self.id}:\n    Name: {self.name}\n    Aisle: {self.aisle.name}(id:{self.aisle.id})\n    Department: {self.department.name}(id:{self.department.id})\n"
