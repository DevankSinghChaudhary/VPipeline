class Car:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed

    def attribute(self):
        print(f"name: {self.name}")
        print(f"speed: {self.speed}")

car = Car("BMW", 400).attribute()
