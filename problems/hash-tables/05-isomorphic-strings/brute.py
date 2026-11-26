class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        def encode(text: str) -> list:
            first = {}
            out = []
            for i, ch in enumerate(text):
                if ch not in first:
                    first[ch] = i
                out.append(first[ch])
            return out

        return encode(s) == encode(t)
