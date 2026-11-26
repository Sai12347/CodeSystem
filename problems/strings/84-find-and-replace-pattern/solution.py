class Solution:
    def findAndReplacePattern(self, words: List[str], pattern: str) -> List[str]:
        def matches(w: str) -> bool:
            p2w = [-1] * 26
            w2p = [-1] * 26
            for pc, wc in zip(pattern, w):
                pi, wi = ord(pc) - 97, ord(wc) - 97
                if p2w[pi] == -1 and w2p[wi] == -1:
                    p2w[pi] = wi
                    w2p[wi] = pi
                elif p2w[pi] != wi or w2p[wi] != pi:
                    return False
            return True
        return [w for w in words if matches(w)]
