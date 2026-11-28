class Circle:
    def __init__(self, radius):
        self.radius = radius
    def calculate_area(self):
        print(self.radius * self.radius * 3.14)
    def calculate_circumference(self):
        print(self.radius * 3.14 * 2)
circle_1 = Circle(5)
circle_2 = Circle(22)
circle_1.calculate_area()
circle_1.calculate_circumference()
circle_2.calculate_area()
circle_2.calculate_circumference()