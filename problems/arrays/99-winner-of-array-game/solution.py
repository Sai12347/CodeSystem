class Solution:
    def getWinner(self, arr: List[int], k: int) -> int:
        champion = arr[0]
        wins = 0
        for x in arr[1:]:
            if champion > x: wins += 1
            else: champion, wins = x, 1
            if wins == k: return champion
        return champion
