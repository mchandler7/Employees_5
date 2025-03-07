"""
Student information for this assignment:

Replace <FULL NAME> with your name.
On my/our honor, Matthew Chandler and Issac Koshy, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1:mec5767
UT EID 2:isk333
"""

from abc import ABC, abstractmethod
import random

DAILY_EXPENSE = 60
HAPPINESS_THRESHOLD = 50
MANAGER_BONUS = 1000
TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD = 50
PERM_EMPLOYEE_PERFORMANCE_THRESHOLD = 25
RELATIONSHIP_THRESHOLD = 10
INITIAL_PERFORMANCE = 75
INITIAL_HAPPINESS = 50
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
SALARY_ERROR_MESSAGE = "Salary must be non-negative."



class Employee(ABC):
    """
    Abstract base class representing a generic employee in the system.
    """

    def __init__(self, name, manager, salary, savings):
        self.relationships = {}
        self.savings = savings
        self.is_employed = True
        self.__name = name
        self.__manager = manager
        self.performance = INITIAL_PERFORMANCE
        self.happiness = INITIAL_HAPPINESS
        self.salary = salary
    @property
    def name(self):
        """
        Property that gives access to the read-only name attribute.
        """
        return self.__name
    @property
    def manager(self):
        """
        Returns read-only attribute for manager.
        """
        return self.__manager
    @property
    def performance(self):
        """
        Returns read-only attribute for performance.
        """
        return self.__performance
    @property
    def happiness(self):
        """
        Returns read-only attribute for happiness.
        """
        return self.__happiness
    @property
    def salary(self):
        """
        Returns read-only attribute for salary.
        """
        return self.__salary
    @performance.setter
    def performance(self,new_performance):
        if PERCENTAGE_MIN <= new_performance <= PERCENTAGE_MAX:
            self.__performance = new_performance
        elif new_performance < PERCENTAGE_MIN:
            self.__performance = 0
        elif new_performance > PERCENTAGE_MAX:
            self.__performance = 100
    @happiness.setter
    def happiness(self, new_happiness):
        if PERCENTAGE_MIN <= new_happiness <= PERCENTAGE_MAX:
            self.__happiness = new_happiness
        elif new_happiness < PERCENTAGE_MIN:
            self.__happiness = 0
        elif new_happiness > PERCENTAGE_MAX:
            self.__happiness = 100
    @salary.setter
    def salary(self, new_salary):
        if new_salary >= 0:
            self.__salary = new_salary
        else:
            raise ValueError(SALARY_ERROR_MESSAGE)
    @abstractmethod
    def work(self):
        """
        Abstract method for employee indicating work
        """
        #pass
    def interact(self, other):
        """
        Initiates the relationship initially or increases or decreases the relationship value
        """
        if other.name not in self.relationships:
            self.relationships[other.name] = 0
        if self.relationships[other.name] > RELATIONSHIP_THRESHOLD:
            self.happiness += 1
        elif self.happiness >= HAPPINESS_THRESHOLD and other.happiness >= HAPPINESS_THRESHOLD:
            self.relationships[other.name] += 1
        else:
            self.relationships[other.name] -= 1
            self.happiness -= 1
    def daily_expense(self):
        """
        Reduces happiness by one and reduces savings by daily expenses
        """
        self.happiness -= 1
        self.savings -= DAILY_EXPENSE
    def __str__(self):
        f_half = f'{self.name}\n\tSalary: ${self.salary}\n\tSavings: ${self.savings}\n\tHappiness:'
        return f'{f_half} {self.happiness/100:.0%}\n\tPerformance: {self.performance/100:.0%}'

class Manager(Employee):
    """
    A subclass of Employee representing a manager.
    """
    def work(self):
        change = random.randint(-5,5)
        self.performance += change
        if change <= 0:
            self.happiness -= 1
            for person in self.relationships:
                self.relationships[person] -= 1

        else:
            self.happiness += 1


class TemporaryEmployee(Employee):
    """
    A subclass of Employee representing a temporary employee.
    """
    def work(self):
        change = random.randint(-15,15)
        self.performance += change
        if change <= 0:
            self.happiness -= 2
        else:
            self.happiness += 1
    def interact(self, other):
        super().interact(other)
        if isinstance(other, Manager) and self.manager == other:
            if other.happiness > HAPPINESS_THRESHOLD:
                if self.performance >= TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD:
                    self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.salary //= 2
                self.happiness -= 5
            if self.salary == 0:
                self.is_employed = False


class PermanentEmployee(Employee):
    """
    A subclass of Employee representing a permanent employee.
    """
    def work(self):
        change = random.randint(-10,10)
        self.performance += change
        if change >= 0:
            self.happiness += 1
    def interact(self, other):
        super().interact(other)
        if isinstance(other, Manager) and self.manager == other:
            if other.happiness > HAPPINESS_THRESHOLD:
                if self.performance >= PERM_EMPLOYEE_PERFORMANCE_THRESHOLD:
                    self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.happiness -= 1
