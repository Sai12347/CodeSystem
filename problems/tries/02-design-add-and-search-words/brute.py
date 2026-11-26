class WordDictionary:
    def __init__(self) -> None:
        self.by_len = defaultdict(set)

    def addWord(self, word: str) -> None:
        self.by_len[len(word)].add(word)

    def search(self, word: str) -> bool:
        for candidate in self.by_len[len(word)]:
            if all(a == "." or a == b for a, b in zip(word, candidate)):
                return True
        return False
