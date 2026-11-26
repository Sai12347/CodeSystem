class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []
        word_len = len(words[0])
        num_words = len(words)
        total_len = word_len * num_words
        n = len(s)
        if n < total_len:
            return []

        need = Counter(words)
        result = []

        for offset in range(word_len):
            left = offset
            seen = defaultdict(int)
            matched = 0
            for right in range(offset, n - word_len + 1, word_len):
                word = s[right:right + word_len]
                if word in need:
                    seen[word] += 1
                    matched += 1
                    while seen[word] > need[word]:
                        left_word = s[left:left + word_len]
                        seen[left_word] -= 1
                        matched -= 1
                        left += word_len
                    if matched == num_words:
                        result.append(left)
                        left_word = s[left:left + word_len]
                        seen[left_word] -= 1
                        matched -= 1
                        left += word_len
                else:
                    seen.clear()
                    matched = 0
                    left = right + word_len

        return result
