class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        roots = set(dictionary)
        out = []
        for word in sentence.split(" "):
            rep = word
            for i in range(1, len(word) + 1):
                if word[:i] in roots:
                    rep = word[:i]
                    break
            out.append(rep)
        return " ".join(out)
