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

class Dog:
    def __init__(self, name, breed):
       self.name = name
       self.breed = breed
    def display(self):
       print("\nDog Details")
       print("Name:", self.name)
       print("Breed:", self.breed)
    def barks(self):
       print("Woof Woof!")
Dog_1 = Dog("Tuffy", "French Bulldog")
Dog_2 = Dog("Max", "Labrador Retriever")
Dog_1.display()
Dog_2.display()
Dog_1.barks()
Dog_2.barks()