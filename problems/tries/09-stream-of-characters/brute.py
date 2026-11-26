class StreamChecker:
    def __init__(self, words: List[str]) -> None:
        self.words = list(set(words))
        self.stream = ""

    def query(self, letter: str) -> bool:
        self.stream += letter
        return any(self.stream.endswith(w) for w in self.words)
