class Solution:
    def detectLCGCycle(self, a: int, c: int, m: int, seed: int) -> List[int]:
        def step(x: int) -> int:
            return (a * x + c) % m

        x0 = seed % m
        tortoise = step(x0)
        hare = step(step(x0))
        while tortoise != hare:
            tortoise = step(tortoise)
            hare = step(step(hare))

        mu = 0
        tortoise = x0
        while tortoise != hare:
            tortoise = step(tortoise)
            hare = step(hare)
            mu += 1

        lam = 1
        hare = step(tortoise)
        while tortoise != hare:
            hare = step(hare)
            lam += 1
        return [mu, lam]
