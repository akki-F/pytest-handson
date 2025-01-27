class Calculator:
    def add(self, x, y):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            raise ValueError("Invalid input")
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        return x / y

    def complex_operation(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Input must be a number")
        if value < 0:
            raise ValueError("Value must be positive")
        return value * 2
