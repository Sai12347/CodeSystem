class Solution:
    def deckRevealedIncreasing(self, deck: List[int]) -> List[int]:
        dq = deque()
        for card in sorted(deck, reverse=True):
            if dq:
                dq.appendleft(dq.pop())
            dq.appendleft(card)
        ans = list(dq)
        sim = deque(ans)
        revealed = []
        while sim:
            revealed.append(sim.popleft())
            if sim:
                sim.append(sim.popleft())
        assert revealed == sorted(deck)
        return ans
