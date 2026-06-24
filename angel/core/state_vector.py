class PersonalState:
    def __init__(self):
        self.data = {}
    def update(self, source, data):
        self.data[source] = data
