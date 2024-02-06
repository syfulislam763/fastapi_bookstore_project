class UnicornException(Exception):
    def __init__(self, id:int):
        self.id = id

class TestException(Exception):
    def __init__(self, id:int, msg:str):
        self.id = id
        self.msg = msg