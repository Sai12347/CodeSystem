class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0
        word_set.discard(beginWord)
        word_set.discard(endWord)

        front = {beginWord}
        back = {endWord}
        length = 1
        word_len = len(beginWord)
        letters = "abcdefghijklmnopqrstuvwxyz"

        while front and back:
            if len(front) > len(back):
                front, back = back, front
            next_front = set()
            for word in front:
                for i in range(word_len):
                    prefix = word[:i]
                    suffix = word[i + 1:]
                    orig_ch = word[i]
                    for ch in letters:
                        if ch == orig_ch:
                            continue
                        cand = prefix + ch + suffix
                        if cand in back:
                            return length + 1
                        if cand in word_set:
                            word_set.remove(cand)
                            next_front.add(cand)
            front = next_front
            length += 1

        return 0
