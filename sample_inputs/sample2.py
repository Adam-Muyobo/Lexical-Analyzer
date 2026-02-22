class Person:
    def __init__(self, name):
        self.name = name  # store name
    def greet(self):
        return "Hello, " + self.name

p = Person("Tida")
print(p.greet())
