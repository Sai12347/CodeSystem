class Logger:
    def __init__(self):
        self.next_ok = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if timestamp < self.next_ok.get(message, -1):
            return False
        self.next_ok[message] = timestamp + 10
        return True
