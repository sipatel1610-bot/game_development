class Student:
    def __init__(self, name, age, course, marks):
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks
    def display(self):
        print("\nStudent Details")
        print("Name:", self.name)
        print("Age:", self.age)
        print("Course:", self.course)
        print("Marks:", self.marks)
    def average(self):
        avg = sum(self.marks)/len(self.marks)
        print("average marks:", avg)
Student_1 = Student("Alex", 19, "Maths", [83, 91, 89])
Student_2 = Student("Ben", 18, "Science", [43, 64, 59])
Student_1.display()
Student_1.average()
Student_2.display()
Student_2.average()