class Solution:
    def findOriginalArray(self, changed: List[int]) -> List[int]:
        if len(changed) % 2: return []
        counts = Counter(changed)
        answer = []
        for x in sorted(changed):
            if counts[x] == 0: continue
            if x == 0:
                if counts[x] < 2: return []
                counts[x] -= 2; answer.append(0); continue
            if counts[2*x] == 0: return []
            counts[x] -= 1; counts[2*x] -= 1; answer.append(x)
        return answer if len(answer) * 2 == len(changed) else []
