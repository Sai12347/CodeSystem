class Solution:
    def mostVisitedPattern(self, username: List[str], timestamp: List[int], website: List[str]) -> List[str]:
        by_user = defaultdict(list)
        for u, t, w in zip(username, timestamp, website):
            by_user[u].append((t, w))

        scores = Counter()
        for visits in by_user.values():
            visits.sort(key=lambda x: x[0])
            sites = [w for _, w in visits]
            m = len(sites)
            seen = set()
            for i in range(m):
                for j in range(i + 1, m):
                    for k in range(j + 1, m):
                        seen.add((sites[i], sites[j], sites[k]))
            for pat in seen:
                scores[pat] += 1

        best_pat = min(scores.keys(), key=lambda p: (-scores[p], p))
        return list(best_pat)
