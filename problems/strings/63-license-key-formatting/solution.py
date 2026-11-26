class Solution:
    def licenseKeyFormatting(self, s: str, k: int) -> str:
        clean = s.replace("-", "").upper()
        if not clean:
            return ""
        first = len(clean) % k or k
        parts = [clean[:first]]
        for i in range(first, len(clean), k):
            parts.append(clean[i:i + k])
        return "-".join(parts)
