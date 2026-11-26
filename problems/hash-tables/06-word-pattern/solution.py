class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(" ")
        if len(words) != len(pattern):
            return False
        char_to_word = {}
        word_to_char = {}
        for ch, w in zip(pattern, words):
            if ch in char_to_word:
                if char_to_word[ch] != w:
                    return False
            elif w in word_to_char:
                return False
            else:
                char_to_word[ch] = w
                word_to_char[w] = ch
        return True
