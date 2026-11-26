class Solution:
    def findLadders(
        self, beginWord: str, endWord: str, wordList: List[str]
    ) -> List[List[str]]:
        word_set = set(wordList)
        if endWord not in word_set:
            return []

        word_set.discard(beginWord)
        parents: defaultdict[str, List[str]] = defaultdict(list)
        layer = {beginWord}
        found = False
        word_len = len(beginWord)
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        while layer and not found:
            next_layer = set()
            for word in layer:
                for i in range(word_len):
                    prefix = word[:i]
                    suffix = word[i + 1 :]
                    orig = word[i]
                    for ch in alphabet:
                        if ch == orig:
                            continue
                        nxt = prefix + ch + suffix
                        if nxt in word_set:
                            parents[nxt].append(word)
                            next_layer.add(nxt)
                            if nxt == endWord:
                                found = True
            word_set -= next_layer
            layer = next_layer

        if not found:
            return []

        res: List[List[str]] = []
        path = [endWord]

        def backtrack(word: str) -> None:
            if word == beginWord:
                res.append(path[::-1])
                return
            for p in parents[word]:
                path.append(p)
                backtrack(p)
                path.pop()

        backtrack(endWord)
        return res
