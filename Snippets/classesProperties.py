
# PYTHON CLASSES:
# Code snippets and notes
# from Corey Schafer's Python OOP YouTube series:
# Tutorial 1: Classes and Instances https://youtu.be/ZDa-Z5JzLYM
# Tutorial 2: Class Variables https://youtu.be/BJ-VvGyQxho
# Tutorial 3: Classmethods and Staticmethods https://youtu.be/rq8cL2XMM5M
# Tutorial 4: Inheritance and Subclasses https://youtu.be/RSl87lqOXDE
# Tutorial 5: Special (Magic Methods, Dunder Methods) https://youtu.be/3ohzBxoFHAY
# Tutorial 6: Property Decorators, Getters, Setters

# Generate a class called employee that stores information on people
# PEP-8 naming conventions -> class names are title case
class Employee:
    # These variables are shared among instances. This can be overwritten
    # in the event that an individual must have a variable that has the
    # same name and a different value. For instance, it is possible to
    # have an instance with a different raise_amt than the others in this
    # class by declaring it separately.
    num_of_emps = 0
    raise_amt = 1.04
    # This runs when an instance is created
    # The first argument is always self, followed by any
    # variables you would like to pass into the first instance
    def __init__(self, firstname, lastname, salary):
        # Use the self method to assign firstname to this instance
        # of employee upon creation
        self.first = firstname
        self.last = lastname
        self.pay = salary
        # Modify class variables that exist for all instances within the
        # class
        Employee.num_of_emps += 1
    # functions can take arguments and set or return information
    def apply_raise(self, bonus):
        self.pay = int(self.pay * self.raise_amt)
        print("{} {} receives a bonus of $ {} ".format(self.first, self.last, bonus))
    # This is a decorator that defines a method which we can 
    # access similar to a property. If we were to omit the
    # @property line decorator so that a call for this method
    # does not need the parentheses afterward
    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)
    
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    # This is a setter used to pass the full name in as a string
    # and splits on the space between names but only works
    # for instances that are already created
    @fullname.setter
    def fullname(self, name):
        first_n, last_n = name.split(' ')
        self.first = first_n
        self.last = last_n
    # This is run when an instance is deleted from the class
    @fullname.deleter
    def fullname(self):
        print('Deleting Name!')
        self.first = None
        self.last = None
        self.pay = None
        Employee.num_of_emps -= 1
    # Here is a way to change the raise amount for the
    # entire class and every instance within the class. The first
    # argument is always named 'cls' by naming convention
    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amt = amount
    # An example of using the class argument to input a string
    # and generate a class from parsing the information
    @classmethod
    def from_string(cls, emp_str):
        # Parse out the first, last, and pay from a string that
        # breaks along the spaces
        first, last, pay = emp_str.split(' ')
        # Generate an instance of the class by passing the 
        # nessecary arguments into the init method.
        return cls(first, last, pay)
    # Functions and init methods need "self" passed as the first argument,
    # Class methods need the "cls" passed as the first argument
    # Static methods need neither. These are only included if they make
    # some logical sense to include these functions within the class.
    @staticmethod
    def is_workday(day):
        # The datetime module has a weekday method that evaluates the
        # Monday = 0, Tuesday = 1,...,Sunday = 6
        if day.weekday() == 5 or day.weekday() == 6:
            # If the date passed into the the is_workday function is on
            # Saturday or Sunday, return False, the day is on a weekend.
            return False
        # This belongs as a static method because it does not take any
        # arguments to or from the instances contained within Employee
        return True
    # Normally when we just call print(emp_1) we get 'instance of class Employee...'
    # and this is usually not too helpful. By including these dunder statements, we
    # can get more information from an instance call to print.
    def __repr__(self):
        # Dunder repr is the coders version to generate a string that we
        # could use to recreate the object.
        return "Employee('{}', '{}', '{}')".format(self.first, self.last, self.pay)
    def __str__(self):
        # Dunder str is the user friendly string representation of the instance
        return '{} - {}'.format(self.fullname, self.email)
    # Use dunder add to tell python how to add the employees together
    def __add__(self, other):
        return '{}-{}'.format(self.last, other.last)
    # This dunder statement modifies the way the length command should handle instances
    # of this class
    def __len__(self):
        return len(self.email)
# This is a subclass of Employee. supervisors still need emails and usernames
# but the subclasses can make modifications 
class Supervisor(Employee):
    raise_amt = 1.10
    # What if we want to define more information for the supervisor
    # than we would need for regular employees?
    def __init__(self, first, last, pay, prog_lang):
        # Pass the first three arguments into the parent class init method.
        super().__init__(first, last, pay)
        # Equivalent code but allows a little more fine tuning if generating an
        # instance in a second parent
        # Employee.__init(self, first, last, pay)
        self.prog_lg = prog_lang

class Manager(Employee):
    # In this case, the last argument is a list of the employees that the manager
    # supervises. This last argument is optional, if nothing is provided, then
    # return a 'None' type.
    def __init__(self, first, last, pay, employees=None):
        # Just as before, let the parent class handle these inputs
        super().__init__(first, last, pay)
        # Check to see if the instantiation received information on subordinates
        if employees is None:
            # Create an empty list if nothing came in
            self.employees = []
        else:
            # Otherwise, set the employee variable to the input
            self.employees = employees
    # Example function ignores duplicate entries    
    def add_employee(self, emp):
        if emp not in self.employees:
            self.employees.append(emp) 
    # Here is how to remove an employee from a managers roster
    def remove_employee(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)        
    # Iterating through the contents of the employees list
    def print_emps(self):
        for emp in self.employees:
            print('-->', emp.fullname)

# Generate an instance of Employee stored in emp_1
emp_1 = Employee('John', 'Smith', 10000)
# OLD VERSION: Employees must be instantiated before settings
# can be changed using the setter or deleter
emp_2 = Employee('Jon', 'Doe', 50000)
# Using the setter to change the name information
emp_2.fullname = 'Clay Freeman'
# Calling a function within the class on employee 2
emp_2.apply_raise(1000)
# Uses the class method to set the raise amount for the entire
# class instead of changing it instance by instance
Employee.set_raise_amount(1.05)
# Generates an instance of raise amount for only employee 2
emp_2.raise_amt = 1.06
print(emp_2.pay)
emp_str_3 = 'Mickey Mouse 5000'
emp_3 = Employee.from_string(emp_str_3)


# print(Employee.raise_amt)
# print(emp_1.raise_amt)
# print(emp_2.raise_amt)
# print(emp_2.raise_amt)
# print(Employee.raise_amt)
# print(emp_1.first)
# print(emp_1.email)
# print(emp_1.fullname)
# print(emp_2.email)

# del emp_1.fullname

# print(emp_3.email)
# print(Employee.num_of_emps)
# print(Employee.__dict__)
# import datetime
# my_date = datetime.date(2018, 1, 29)
# print(Employee.is_workday(my_date))

# The parent class is employee, subclass is suupervisor.
sup_1 = Supervisor('Lauren', 'Greer', 100000, 'French')
sup_2 = Supervisor('Ogden D.', 'Dog', 2, 'arf')
mgr_1 = Manager('Bob', 'Jones', 3, [sup_1])
mgr_1.add_employee(sup_2)
mgr_1.print_emps()
print(emp_1)
# Returns the command that would generate an instance of this class.
print(emp_2.__repr__())
# Returns the front facing string
print(emp_2.__str__())
print(1+2)
print(int.__add__(1, 2))
print(str.__add__('a', ' b'))
# The Dunder Add method describes what to do when two instances of a class are added
# There are many other instances of using arithmetic in these dunders
print(sup_1+emp_2)
# The magic methods modify the way that some commands interact with the class
print(len(sup_2))