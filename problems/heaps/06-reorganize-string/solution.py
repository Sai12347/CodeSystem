class Solution:
    def reorganizeString(self, s: str) -> str:
        n = len(s)
        counts = Counter(s)
        if max(counts.values()) > (n + 1) // 2:
            return ""
        heap = [(-cnt, ch) for ch, cnt in counts.items()]
        heapq.heapify(heap)
        res = []
        prev_cnt, prev_ch = 0, ""
        while heap:
            cnt, ch = heapq.heappop(heap)
            res.append(ch)
            if prev_cnt < 0:
                heapq.heappush(heap, (prev_cnt, prev_ch))
            prev_cnt, prev_ch = cnt + 1, ch
        return "".join(res)
