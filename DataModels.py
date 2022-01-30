import json


class Aisle():
    '''
    Aisle data model
    '''
    id: int
    name: str

    def __init__(self,id:int, name:str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Aisle {self.id}: {self.name}\n"

    def reprJSON(self):
        return dict(id=self.id, name=self.name)



class Department():
    '''
    Department data model
    '''
    id: int
    name: str

    def __init__(self,id:int, name:str):
        self.id = id
        self.name = name
            
    def __repr__(self):
        return f"Department {self.id}: {self.name}\n"

    def reprJSON(self):
        return dict(id=self.id, name=self.name)


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

    def reprJSON(self):
        return dict(id=self.id, name=self.name, aisle=self.aisle, department=self.department)


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
    product_list: list

    def __init__(self, id: int, user_id: int, eval_set: str, order_number: int, order_dow: int, order_hour_of_day: int, days_since_prior_order: int):
        self.id = id
        self.user_id = user_id
        self.eval_set = eval_set
        self.order_number = order_number
        self.order_dow = order_dow
        self.order_hour_of_day = order_hour_of_day
        self.days_since_prior_order = days_since_prior_order
        self.product_list = []

    def __repr__(self):
        return f"Order {self.id}: num of products - {len(self.product_list)}\n"

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def addProduct(self, product: Product):
        self.product_list.append(product)

    def reprJSON(self):
        return dict(id=self.id, user_id = self.user_id, eval_set=self.eval_set, order_number=self.order_number, order_dow=self.order_dow,
            order_hour_of_day=self.order_hour_of_day, days_since_prior_order=self.days_since_prior_order, product_list=self.product_list)
