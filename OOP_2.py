class Calculator:
    def __init__(self, Number_1, Number_2):
        self.Number_1 = Number_1
        self.Number_2 = Number_2
    def add(self):
        print(self.Number_1 + self.Number_2)
    def subtract(self):
        print(self.Number_1 - self.Number_2)
    def multiply(self):
        print(self.Number_1 * self.Number_2)
    def divide(self):
        print(self.Number_1 / self.Number_2)
calc = Calculator(8,4)
calc.add()
calc.subtract()
calc.multiply()
calc.divide()
calc_2 = Calculator(89345,1243543)
calc_2.add()
calc_2.subtract()
calc_2.multiply()
calc_2.divide()