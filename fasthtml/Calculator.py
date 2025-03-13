class Calculator:
    def __init__(self, log):
        self.log = log

    def add(self, a, b):
        result = a + b
        self.log.add_entry(f"add({a}, {b}) = {result}")
        return result

    def subtract(self, a, b):
        result = a - b
        self.log.add_entry(f"subtract({a}, {b}) = {result}")
        return result

    def multiply(self, a, b):
        result = a * b
        self.log.add_entry(f"multiply({a}, {b}) = {result}")
        return result

    def division(self, a, b):
        if b == 0:
            self.log.add_entry(f"divide({a}, {b}) = Error (Cannot divide by zero)")
            return "Error: Cannot divide by zero"
        result = a / b
        self.log.add_entry(f"divide({a}, {b}) = {result}")
        return result

    def show_log(self):
        return self.log.show_logs()

    def delete_log(self, record):
        return self.log.delete_logs(record)
    

    