class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        words = list(dict.fromkeys([beginWord] + wordList))
        idx = {w: i for i, w in enumerate(words)}
        n = len(words)
        L = len(beginWord)
        buckets = defaultdict(list)
        for i, w in enumerate(words):
            for pos in range(L):
                buckets[w[:pos] + "*" + w[pos + 1:]].append(i)

        target = idx[endWord]
        dist = [-1] * n
        dist[0] = 1
        q = deque([0])
        while q:
            u = q.popleft()
            if u == target:
                return dist[u]
            w = words[u]
            for pos in range(L):
                key = w[:pos] + "*" + w[pos + 1:]
                for v in buckets[key]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        q.append(v)
                buckets[key] = []
        return 0
