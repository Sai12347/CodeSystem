class Solution:
    def decodeXoredArray(self, encoded: List[int], first: int) -> List[int]:
        arr = [first] * (len(encoded) + 1)
        for i, v in enumerate(encoded):
            arr[i + 1] = arr[i] ^ v
        return arr
