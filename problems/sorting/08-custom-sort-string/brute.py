class Solution:
    def customSortString(self, order: str, s: str) -> str:
        rank = {ch: i for i, ch in enumerate(order)}
        return "".join(sorted(s, key=lambda ch: rank.get(ch, 26)))
