class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # Independent sweep-line via separate sorted starts and ends
        starts = sorted(iv[0] for iv in intervals)
        ends = sorted(iv[1] for iv in intervals)
        rooms = 0
        max_rooms = 0
        e_idx = 0
        for s in starts:
            while ends[e_idx] <= s:
                rooms -= 1
                e_idx += 1
            rooms += 1
            if rooms > max_rooms:
                max_rooms = rooms
        return max_rooms
