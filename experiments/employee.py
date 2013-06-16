import sys

class Employee(object):
    
    #Class variable section
    
    #List Containing our Employee's.
    employees = []
    
    @classmethod
    def add_employee(cls, employee):
        cls.employees.append(employee)
        #sort the list.
        cls.employees.sort(key = lambda x: x.last)
        
    @classmethod
    def remove_employee(cls, employee):
        """ Remove the employee from the list.  """
        cls.employees.remove(employee)
    
    @classmethod
    def print_employees(cls):
        for i in cls.employees:
            print i.first, i.last

#-------------------------------------------------

    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.add_employee(self)
        
    def change_first_name(self, first):
        self.first = first
        
    def change_last_name(self, last):
        self.last = last
    
    def delete(self):
        """  Delete this employee object. """
        # Delete from the list first.
        self.remove_employee(self)
        #Is this the problem?
        del self
        
if __name__ == "__main__":
    
    employee_1 = Employee("Brent", "Hamby")
    employee_2 = Employee("Seth", "Mcnish")
    employee_3 = Employee("Matt", "Chalker")
    
    print "First printing of the list.  All three should display."
    Employee.print_employees()

    #This is the problem child.
    employee_3.delete()
    #print sys.getrefcount(employee_3)

    print "Employee three deleted.  Print list again."    
    Employee.print_employees()
   
    print "Attempt to print deleted employee, should error out, but it prints." 
    print employee_3.last
    
    print "Let's Delete it outright - that works"
    del employee_3
    print employee_3.last
    
    exit()   