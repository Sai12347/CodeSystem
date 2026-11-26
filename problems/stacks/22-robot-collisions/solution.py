class Solution:
    def survivedRobotsHealths(self, positions: List[int], healths: List[int], directions: str) -> List[int]:
        n = len(positions)
        hp = list(healths)
        order = sorted(range(n), key=lambda i: positions[i])
        stack = []
        for idx in order:
            if directions[idx] == 'R':
                stack.append(idx)
            else:
                while stack and hp[idx] > 0:
                    top = stack[-1]
                    if hp[top] < hp[idx]:
                        stack.pop()
                        hp[top] = 0
                        hp[idx] -= 1
                    elif hp[top] > hp[idx]:
                        hp[top] -= 1
                        hp[idx] = 0
                    else:
                        stack.pop()
                        hp[top] = 0
                        hp[idx] = 0
        return [h for h in hp if h > 0]
