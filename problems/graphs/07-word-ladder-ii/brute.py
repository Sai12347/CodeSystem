class Solution:
    def findLadders(
        self, beginWord: str, endWord: str, wordList: List[str]
    ) -> List[List[str]]:
        word_set = set(wordList)
        if endWord not in word_set:
            return []

        def differs_by_one(a: str, b: str) -> bool:
            diff = 0
            for x, y in zip(a, b):
                if x != y:
                    diff += 1
                    if diff > 1:
                        return False
            return diff == 1

        all_words = list(word_set | {beginWord})
        adj = defaultdict(list)
        for i in range(len(all_words)):
            for j in range(i + 1, len(all_words)):
                if differs_by_one(all_words[i], all_words[j]):
                    adj[all_words[i]].append(all_words[j])
                    adj[all_words[j]].append(all_words[i])

        level_paths = [[beginWord]]
        visited = {beginWord}
        res = []

        while level_paths and not res:
            next_level = []
            level_seen = set()
            for path in level_paths:
                last = path[-1]
                for nxt in adj[last]:
                    if nxt in visited:
                        continue
                    new_path = path + [nxt]
                    if nxt == endWord:
                        res.append(new_path)
                    else:
                        next_level.append(new_path)
                        level_seen.add(nxt)
            visited |= level_seen
            level_paths = next_level

        return res
