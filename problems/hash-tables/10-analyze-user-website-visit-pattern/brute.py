from itertools import combinations


class Solution:
    def mostVisitedPattern(self, username: List[str], timestamp: List[int], website: List[str]) -> List[str]:
        records = sorted(zip(timestamp, username, website))
        user_sites = defaultdict(list)
        for _, u, w in records:
            user_sites[u].append(w)

        pattern_users = defaultdict(set)
        for u, sites in user_sites.items():
            for pat in combinations(sites, 3):
                pattern_users[pat].add(u)

        best = None
        best_score = -1
        for pat, users in pattern_users.items():
            score = len(users)
            if score > best_score or (score == best_score and pat < best):
                best_score = score
                best = pat
        return list(best)
