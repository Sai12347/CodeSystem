class Solution:
    def reorganizeString(self, s: str) -> str:
        counts = Counter(s)
        out = []
        previous = ''
        while len(out) < len(s):
            choices = [c for c in counts if counts[c] and c != previous]
            if not choices: return ''
            c = min(choices, key=lambda x: (-counts[x], x))
            out.append(c); counts[c] -= 1; previous = c
        return ''.join(out)
