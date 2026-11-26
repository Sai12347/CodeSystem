class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)
        stack = []  # (dist, speed) representing time = dist / speed
        for pos, spd in cars:
            dist = target - pos
            if not stack or dist * stack[-1][1] > stack[-1][0] * spd:
                stack.append((dist, spd))
        return len(stack)
