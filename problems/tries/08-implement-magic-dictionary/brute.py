class MagicDictionary:
    def __init__(self) -> None:
        self.words = []

    def buildDict(self, dictionary: List[str]) -> None:
        self.words = list(dictionary)

    def search(self, searchWord: str) -> bool:
        n = len(searchWord)
        for w in self.words:
            if len(w) == n and sum(a != b for a, b in zip(w, searchWord)) == 1:
                return True
        return False
