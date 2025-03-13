class Log:
    def __init__(self):
        self.logs = []

    def add_entry(self, entry):
        self.logs.append(entry)

    def show_logs(self):
        return self.logs
    
    def delete_logs(self,item):
        return self.logs.pop(item)
    