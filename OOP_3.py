class Car:
    def __init__(self, brand, model, color):
        self.brand = brand
        self.model = model
        self.color = color
    def start(self):
        print("The car has started")
    def display_details(self):
        print("Car Details")
        print("Brand:", self.brand)
        print("Model:", self.model)
        print("Color:", self.color)
Car_1 = Car("BMW", "M4", "Black")
Car_2 = Car("Tata", "Harrier", "Blue")
Car_1.display_details()
Car_1.start()
Car_2.display_details()
Car_2.start()