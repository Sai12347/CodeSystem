#!/usr/bin/env python3
"""Generate string problems 71-100 for AlgoPlay."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "problems" / "strings"


def py_type(t: str) -> str:
    if t == "void":
        return "None"
    if t.endswith("[]"):
        return f"List[{py_type(t[:-2])}]"
    if t.startswith("List<") and t.endswith(">"):
        return f"List[{py_type(t[5:-1])}]"
    return {
        "int": "int",
        "long": "int",
        "double": "float",
        "boolean": "bool",
        "char": "str",
        "String": "str",
    }[t]


TASKS = [
    {
        "slug": "71-number-of-substrings-containing-all-three-chars",
        "title": "Number of Substrings Containing All Three Characters",
        "difficulty": "Medium",
        "subtopic": "Substrings",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": "Given a string `s` consisting only of the characters `'a'`, `'b'`, and `'c'`, return the total number of contiguous substrings that contain at least one occurrence of all three characters `'a'`, `'b'`, and `'c'`.",
        "cons": ["3 <= s.length <= 5 * 10^4", "s consists only of 'a', 'b', or 'c'."],
        "hints": [
            "For every right endpoint i, track the most recent index where each of 'a', 'b', and 'c' appeared.",
            "Any starting index from 0 up to min(lastA, lastB, lastC) forms a valid substring ending at i."
        ],
        "explanations": [
            "There are 10 substrings in \"abcabc\" containing 'a', 'b', and 'c'.",
            "The valid substrings of \"aaacb\" are \"aaacb\", \"aacb\", and \"acb\".",
            "Only the full string \"abc\" contains all three letters."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "numberOfSubstrings",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        last = [-1, -1, -1]
        ans = 0
        for i, ch in enumerate(s):
            last[ord(ch) - 97] = i
            m = min(last)
            if m >= 0:
                ans += m + 1
        return ans""",
        "java": """        int[] last = {-1, -1, -1};
        int ans = 0;
        for (int i = 0; i < s.length(); i++) {
            last[s.charAt(i) - 'a'] = i;
            int m = Math.min(last[0], Math.min(last[1], last[2]));
            if (m >= 0) ans += m + 1;
        }
        return ans;""",
        "visible": [{"s": "abcabc"}, {"s": "aaacb"}, {"s": "abc"}],
        "hidden": [
            {"s": "aaa"},
            {"s": "ababab"},
            {"s": "acbbcac"},
            {"s": "bbbaaac"},
            {"s": "cbacba"},
            {"s": "aabbcc"},
            {"s": "cccbba"},
            {"s": "a" * 500 + "b" + "c" * 500},
            {"s": "abc" * 500},
        ],
    },
    {
        "slug": "72-longest-substring-between-equal-characters",
        "title": "Largest Substring Between Two Equal Characters",
        "difficulty": "Easy",
        "subtopic": "Substrings",
        "companies": ["Amazon", "Adobe", "Bloomberg"],
        "desc": "Given a lowercase string `s`, return the length of the longest contiguous substring strictly between two equal characters (excluding the two equal characters themselves). If no character appears at least twice in `s`, return `-1`.",
        "cons": ["1 <= s.length <= 10^4", "s contains only lowercase English letters."],
        "hints": [
            "To maximize distance between two occurrences of a character, always pair it with its very first occurrence.",
            "Record the first index of each letter in a 26-element array and update max(best, i - first[c] - 1) on later occurrences."
        ],
        "explanations": [
            "Between the two 'a's in \"aa\" lies an empty substring of length 0.",
            "Between the two 'a's in \"abca\" lies \"bc\" of length 2.",
            "All characters in \"cbzxy\" are unique, so return -1."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "maxLengthBetweenEqualCharacters",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        first = [-1] * 26
        best = -1
        for i, ch in enumerate(s):
            idx = ord(ch) - 97
            if first[idx] == -1:
                first[idx] = i
            else:
                best = max(best, i - first[idx] - 1)
        return best""",
        "java": """        int[] first = new int[26];
        Arrays.fill(first, -1);
        int best = -1;
        for (int i = 0; i < s.length(); i++) {
            int idx = s.charAt(i) - 'a';
            if (first[idx] == -1) first[idx] = i;
            else best = Math.max(best, i - first[idx] - 1);
        }
        return best;""",
        "visible": [{"s": "aa"}, {"s": "abca"}, {"s": "cbzxy"}],
        "hidden": [
            {"s": "a"},
            {"s": "cabbac"},
            {"s": "scayofdzca"},
            {"s": "mgntdygtxrvxjnwksqhxuxtrv"},
            {"s": "abcdefg"},
            {"s": "aaaaaaa"},
            {"s": "abacaba"},
            {"s": "a" + "bcdef" * 200 + "a"},
            {"s": "abcdefghijklmnopqrstuvwxyz"},
        ],
    },
    {
        "slug": "73-maximum-vowels-in-substring-of-length-k",
        "title": "Maximum Number of Vowels in a Substring of Given Length",
        "difficulty": "Medium",
        "subtopic": "Substrings",
        "companies": ["Amazon", "Google", "Meta"],
        "desc": "Given a lowercase string `s` and an integer `k`, return the maximum number of vowel letters (`'a'`, `'e'`, `'i'`, `'o'`, `'u'`) contained in any contiguous substring of `s` of length `k`.",
        "cons": ["1 <= s.length <= 10^5", "1 <= k <= s.length", "s consists of lowercase English letters."],
        "hints": [
            "Maintain a fixed-size sliding window of length k.",
            "When advancing by one character, add 1 if the incoming character is a vowel and subtract 1 if the outgoing character at i - k is a vowel."
        ],
        "explanations": [
            "The substring \"iii\" of length 3 contains 3 vowels.",
            "Any length-2 substring of \"aeiou\" contains 2 vowels.",
            "The substring \"lee\" (or \"eet\") of length 3 contains 2 vowels."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "maxVowels",
        "params": [("s", "String"), ("k", "int")],
        "ret": "int",
        "py": """        vowels = set("aeiou")
        cur = 0
        best = 0
        for i, ch in enumerate(s):
            if ch in vowels:
                cur += 1
            if i >= k and s[i - k] in vowels:
                cur -= 1
            if i >= k - 1 and cur > best:
                best = cur
        return best""",
        "java": """        int cur = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            if (isVowel(s.charAt(i))) cur++;
            if (i >= k && isVowel(s.charAt(i - k))) cur--;
            if (i >= k - 1 && cur > best) best = cur;
        }
        return best;
    }
    private boolean isVowel(char c) {
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';""",
        "visible": [
            {"s": "abciiidef", "k": 3},
            {"s": "aeiou", "k": 2},
            {"s": "leetcode", "k": 3},
        ],
        "hidden": [
            {"s": "rhythms", "k": 4},
            {"s": "tryhard", "k": 4},
            {"s": "a", "k": 1},
            {"s": "b", "k": 1},
            {"s": "weallloveyou", "k": 7},
            {"s": "aeiouaeiou", "k": 10},
            {"s": "bcdfghjklmnpqrstvwxyz", "k": 5},
            {"s": "bacadaeafagahaia", "k": 4},
            {"s": "bcdfg" * 400 + "aeiou" * 20 + "bcdfg" * 400, "k": 100},
        ],
    },
    {
        "slug": "74-count-homogenous-substrings",
        "title": "Count Number of Homogenous Substrings",
        "difficulty": "Medium",
        "subtopic": "Substrings",
        "companies": ["Amazon", "Google", "Atlassian"],
        "desc": "A string is homogenous if all characters in it are identical. Given a lowercase string `s`, return the total number of non-empty homogenous contiguous substrings of `s`, modulo `1,000,000,007`.",
        "cons": ["1 <= s.length <= 10^5", "s consists of lowercase English letters."],
        "hints": [
            "A maximal run of length L of the same character contributes L * (L + 1) / 2 homogenous substrings.",
            "Equivalently, track the current run length ending at index i and add it to the total modulo 10^9 + 7."
        ],
        "explanations": [
            "Runs have lengths 3, 2, 1, 2 -> 6 + 3 + 1 + 3 = 13.",
            "Single-character runs \"x\" and \"y\" give 1 + 1 = 2.",
            "A run of 5 'z's contributes 5 * 6 / 2 = 15 substrings."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "countHomogenous",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        mod = 1000000007
        ans = 0
        run = 0
        prev = ""
        for ch in s:
            if ch == prev:
                run += 1
            else:
                run = 1
                prev = ch
            ans = (ans + run) % mod
        return ans""",
        "java": """        final int MOD = 1000000007;
        long ans = 0;
        int run = 0;
        char prev = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == prev) run++;
            else { run = 1; prev = ch; }
            ans = (ans + run) % MOD;
        }
        return (int) ans;""",
        "visible": [{"s": "abbcccaa"}, {"s": "xy"}, {"s": "zzzzz"}],
        "hidden": [
            {"s": "a"},
            {"s": "aa"},
            {"s": "ababab"},
            {"s": "aaabbbccc"},
            {"s": "abccba"},
            {"s": "mississippi"},
            {"s": "a" * 1000},
            {"s": "a" * 5000},
            {"s": "z" * 10000},
        ],
    },
    {
        "slug": "75-longest-even-vowel-counts-substring",
        "title": "Longest Substring Containing Vowels in Even Counts",
        "difficulty": "Medium",
        "subtopic": "Substrings",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": "Given a lowercase string `s`, return the length of the longest contiguous substring in which each of the five vowels `'a'`, `'e'`, `'i'`, `'o'`, and `'u'` appears an even number of times (zero is even).",
        "cons": ["1 <= s.length <= 5 * 10^5", "s contains only lowercase English letters."],
        "hints": [
            "Encode the parity (even/odd) of the 5 vowel counts as a 5-bit integer mask (0..31).",
            "A substring s[l..r] has all even vowel counts iff prefixMask[r + 1] == prefixMask[l]. Store the earliest index seen for each of the 32 masks."
        ],
        "explanations": [
            "\"leetminicowor\" has length 13 and contains 2 'e's, 2 'i's, and 2 'o's (with 0 'a' and 0 'u').",
            "\"leetc\" has length 5 and contains 2 'e's and 0 of the other vowels.",
            "No vowels appear in \"bcbcbc\", so the entire string of length 6 is valid."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "findTheLongestSubstring",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        bit = {'a': 1, 'e': 2, 'i': 4, 'o': 8, 'u': 16}
        first = [-2] * 32
        first[0] = -1
        mask = 0
        best = 0
        for i, ch in enumerate(s):
            mask ^= bit.get(ch, 0)
            if first[mask] == -2:
                first[mask] = i
            else:
                best = max(best, i - first[mask])
        return best""",
        "java": """        int[] first = new int[32];
        Arrays.fill(first, -2);
        first[0] = -1;
        int mask = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == 'a') mask ^= 1;
            else if (c == 'e') mask ^= 2;
            else if (c == 'i') mask ^= 4;
            else if (c == 'o') mask ^= 8;
            else if (c == 'u') mask ^= 16;
            if (first[mask] == -2) first[mask] = i;
            else best = Math.max(best, i - first[mask]);
        }
        return best;""",
        "visible": [
            {"s": "eleetminicoworoep"},
            {"s": "leetcodeisgreat"},
            {"s": "bcbcbc"},
        ],
        "hidden": [
            {"s": "a"},
            {"s": "b"},
            {"s": "aa"},
            {"s": "aeiou"},
            {"s": "aeiouaeiou"},
            {"s": "id"},
            {"s": "aabbccddeeff"},
            {"s": "abecidofu" * 100},
            {"s": "xyz" * 1000 + "a" + "xyz" * 999},
        ],
    },
    {
        "slug": "76-number-of-wonderful-substrings",
        "title": "Number of Wonderful Substrings",
        "difficulty": "Hard",
        "subtopic": "Substrings",
        "companies": ["Google", "Meta", "Uber"],
        "desc": "A wonderful string is a non-empty string where at most one letter appears an odd number of times. Given a string `word` consisting solely of the first ten lowercase English letters (`'a'` through `'j'`), return the number of wonderful non-empty contiguous substrings in `word` as a 64-bit integer. Identical substrings at different index ranges are counted separately.",
        "cons": ["1 <= word.length <= 10^5", "word consists of lowercase English letters from 'a' to 'j'."],
        "hints": [
            "Maintain a 10-bit prefix parity mask for the letters 'a' through 'j' (at most 1024 possible masks).",
            "At each prefix mask m, add count[m] (all-even substrings) plus count[m ^ (1 << b)] for each bit b in 0..9 (exactly one odd-count letter)."
        ],
        "explanations": [
            "The four wonderful substrings of \"aba\" are \"a\", \"b\", \"a\", and \"aba\".",
            "Nine substrings of \"aabb\" have at most one odd-frequency letter.",
            "Only the two single-character substrings \"h\" and \"e\" are wonderful."
        ],
        "time": "O(10 * n)",
        "space": "O(1024)",
        "method": "wonderfulSubstrings",
        "params": [("word", "String")],
        "ret": "long",
        "py": """        cnt = [0] * 1024
        cnt[0] = 1
        mask = 0
        ans = 0
        for ch in word:
            mask ^= 1 << (ord(ch) - 97)
            ans += cnt[mask]
            for b in range(10):
                ans += cnt[mask ^ (1 << b)]
            cnt[mask] += 1
        return ans""",
        "java": """        long[] cnt = new long[1024];
        cnt[0] = 1;
        int mask = 0;
        long ans = 0;
        for (int i = 0; i < word.length(); i++) {
            mask ^= 1 << (word.charAt(i) - 'a');
            ans += cnt[mask];
            for (int b = 0; b < 10; b++) {
                ans += cnt[mask ^ (1 << b)];
            }
            cnt[mask]++;
        }
        return ans;""",
        "visible": [{"word": "aba"}, {"word": "aabb"}, {"word": "he"}],
        "hidden": [
            {"word": "a"},
            {"word": "aa"},
            {"word": "abc"},
            {"word": "abcdefghij"},
            {"word": "fiabhedce"},
            {"word": "abababab"},
            {"word": "aabbccddee"},
            {"word": "a" * 2000},
            {"word": "abcdefghij" * 200},
        ],
    },
    {
        "slug": "77-longest-awesome-palindromic-substring",
        "title": "Find Longest Awesome Substring",
        "difficulty": "Hard",
        "subtopic": "Palindromes",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": "You are given a string `s` consisting only of digits `'0'` through `'9'`. An awesome substring is a non-empty contiguous substring of `s` whose characters can be rearranged (via any number of swaps) to form a palindrome. Return the length of the longest awesome substring of `s`.",
        "cons": ["1 <= s.length <= 10^5", "s consists only of digits '0'-'9'."],
        "hints": [
            "A substring can be rearranged into a palindrome iff at most one digit appears an odd number of times.",
            "Track a 10-bit prefix parity mask and store the earliest index seen for each of the 1024 masks; at each index check mask and mask ^ (1 << d) for d = 0..9."
        ],
        "explanations": [
            "\"24241\" can be rearranged into \"24142\", length 5.",
            "All digits are distinct, so the longest awesome substring has length 1.",
            "\"213123\" can be rearranged into \"231132\", length 6."
        ],
        "time": "O(10 * n)",
        "space": "O(1024)",
        "method": "longestAwesome",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        first = [len(s)] * 1024
        first[0] = -1
        mask = 0
        best = 1
        for i, ch in enumerate(s):
            mask ^= 1 << (ord(ch) - 48)
            if first[mask] == len(s):
                first[mask] = i
            else:
                best = max(best, i - first[mask])
            for d in range(10):
                p = first[mask ^ (1 << d)]
                if p < i:
                    best = max(best, i - p)
        return best""",
        "java": """        int n = s.length();
        int[] first = new int[1024];
        Arrays.fill(first, n);
        first[0] = -1;
        int mask = 0, best = 1;
        for (int i = 0; i < n; i++) {
            mask ^= 1 << (s.charAt(i) - '0');
            if (first[mask] == n) first[mask] = i;
            else best = Math.max(best, i - first[mask]);
            for (int d = 0; d < 10; d++) {
                int p = first[mask ^ (1 << d)];
                if (p < i) best = Math.max(best, i - p);
            }
        }
        return best;""",
        "visible": [{"s": "3242415"}, {"s": "12345678"}, {"s": "213123"}],
        "hidden": [
            {"s": "0"},
            {"s": "00"},
            {"s": "9498331"},
            {"s": "51224"},
            {"s": "0123456789"},
            {"s": "11111"},
            {"s": "12321045654"},
            {"s": "0123456789" * 200},
            {"s": "9" + "012345678" * 100 + "9"},
        ],
    },
    {
        "slug": "78-maximum-score-after-splitting-binary-string",
        "title": "Maximum Score After Splitting a String",
        "difficulty": "Easy",
        "subtopic": "Substrings",
        "companies": ["Amazon", "Microsoft", "Apple"],
        "desc": "Given a binary string `s` of length at least 2 consisting of `'0'` and `'1'`, return the maximum score achievable after splitting `s` into two non-empty substrings (a left prefix and a right suffix). The score of a split is the number of `'0'`s in the left substring plus the number of `'1'`s in the right substring.",
        "cons": ["2 <= s.length <= 10^4", "s[i] is either '0' or '1'."],
        "hints": [
            "Total score = zeros_left + (total_ones - ones_left) = total_ones + (zeros_left - ones_left).",
            "Precompute total_ones (or track zeros_left - ones_left in a single pass up to index n - 2)."
        ],
        "explanations": [
            "Splitting \"011101\" into \"0\" and \"11101\" gives 1 zero + 4 ones = 5.",
            "Splitting \"00111\" into \"00\" and \"111\" gives 2 zeros + 3 ones = 5.",
            "Splitting \"1111\" into \"1\" and \"111\" gives 0 zeros + 3 ones = 3."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "maxScore",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        ones_right = s.count('1')
        zeros_left = 0
        best = 0
        for i in range(len(s) - 1):
            if s[i] == '0':
                zeros_left += 1
            else:
                ones_right -= 1
            best = max(best, zeros_left + ones_right)
        return best""",
        "java": """        int onesRight = 0;
        for (int i = 0; i < s.length(); i++) if (s.charAt(i) == '1') onesRight++;
        int zerosLeft = 0, best = 0;
        for (int i = 0; i < s.length() - 1; i++) {
            if (s.charAt(i) == '0') zerosLeft++;
            else onesRight--;
            best = Math.max(best, zerosLeft + onesRight);
        }
        return best;""",
        "visible": [{"s": "011101"}, {"s": "00111"}, {"s": "1111"}],
        "hidden": [
            {"s": "00"},
            {"s": "01"},
            {"s": "10"},
            {"s": "11"},
            {"s": "00000"},
            {"s": "101010"},
            {"s": "01001"},
            {"s": "0" * 500 + "1" * 500},
            {"s": "1" * 500 + "0" * 500},
        ],
    },
    {
        "slug": "79-count-vowel-substrings-of-a-string",
        "title": "Count Vowel Substrings of a String",
        "difficulty": "Easy",
        "subtopic": "Substrings",
        "companies": ["Amazon", "Google", "Bloomberg"],
        "desc": "A vowel substring is a contiguous substring that consists solely of vowels (`'a'`, `'e'`, `'i'`, `'o'`, `'u'`) and contains all five vowels at least once. Given a lowercase string `word`, return the total number of vowel substrings in `word`.",
        "cons": ["1 <= word.length <= 10^4", "word consists of lowercase English letters only."],
        "hints": [
            "Reset your window whenever you encounter a consonant.",
            "Inside each contiguous vowel run, track the last seen index of each of the 5 vowels; at index i, the number of valid vowel substrings ending at i is max(0, min(lastVowel) - lastConsonant)."
        ],
        "explanations": [
            "\"aeiouu\" has 2 vowel substrings: \"aeiou\" and \"aeiouu\".",
            "No contiguous vowel-only substring contains all 5 vowels.",
            "\"cuaieuouac\" has 7 vowel substrings inside the middle vowel run \"uaieuoua\"."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "countVowelSubstrings",
        "params": [("word", "String")],
        "ret": "int",
        "py": """        vidx = {'a': 0, 'e': 1, 'i': 2, 'o': 3, 'u': 4}
        last_v = [-1] * 5
        last_c = -1
        ans = 0
        for i, ch in enumerate(word):
            if ch in vidx:
                last_v[vidx[ch]] = i
                m = min(last_v)
                if m > last_c:
                    ans += m - last_c
            else:
                last_c = i
        return ans""",
        "java": """        int[] lastV = {-1, -1, -1, -1, -1};
        int lastC = -1, ans = 0;
        for (int i = 0; i < word.length(); i++) {
            int idx = vowelIndex(word.charAt(i));
            if (idx >= 0) {
                lastV[idx] = i;
                int m = lastV[0];
                for (int k = 1; k < 5; k++) m = Math.min(m, lastV[k]);
                if (m > lastC) ans += m - lastC;
            } else {
                lastC = i;
            }
        }
        return ans;
    }
    private int vowelIndex(char c) {
        switch (c) {
            case 'a': return 0;
            case 'e': return 1;
            case 'i': return 2;
            case 'o': return 3;
            case 'u': return 4;
            default: return -1;
        }""",
        "visible": [
            {"word": "aeiouu"},
            {"word": "unicornarihan"},
            {"word": "cuaieuouac"},
        ],
        "hidden": [
            {"word": "a"},
            {"word": "aeiou"},
            {"word": "bbaeixoubb"},
            {"word": "aeio"},
            {"word": "uoiea"},
            {"word": "aaeeiioouu"},
            {"word": "aeioubaeiou"},
            {"word": "aeiou" * 200},
            {"word": "a" * 300 + "eiou" + "b" + "aeiou" * 50},
        ],
    },
    {
        "slug": "80-longest-nice-substring",
        "title": "Longest Nice Substring",
        "difficulty": "Easy",
        "subtopic": "Substrings",
        "companies": ["Microsoft", "Amazon", "Meta"],
        "desc": "A string `s` is nice if for every letter of the alphabet that appears in `s`, both its uppercase and lowercase forms appear in `s`. Given a string `s` of English letters, return the longest contiguous substring of `s` that is nice. If multiple substrings share the maximum length, return the earliest one; if none exist, return `\"\"`.",
        "cons": ["1 <= s.length <= 1000", "s consists of uppercase and lowercase English letters."],
        "hints": [
            "Any character whose opposite-case counterpart is missing from the current range can never be part of a nice substring.",
            "Split the string on any such unpaired character and solve recursively by divide-and-conquer (at most 26 recursion levels)."
        ],
        "explanations": [
            "\"aAa\" has both 'a' and 'A', making it the longest nice substring.",
            "The entire string \"Bb\" is nice.",
            "No letter appears in both cases in \"c\", so return \"\"."
        ],
        "time": "O(n * 26)",
        "space": "O(26)",
        "method": "longestNiceSubstring",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        def solve(l: int, r: int) -> tuple[int, int]:
            if r - l < 2:
                return (0, 0)
            lower = upper = 0
            for i in range(l, r):
                c = ord(s[i])
                if c >= 97:
                    lower |= 1 << (c - 97)
                else:
                    upper |= 1 << (c - 65)
            good = lower & upper
            start = l
            best = (0, 0)
            has_bad = False
            for i in range(l, r):
                c = ord(s[i])
                bit = 1 << (c - 97 if c >= 97 else c - 65)
                if not (good & bit):
                    has_bad = True
                    cand = solve(start, i)
                    if cand[1] - cand[0] > best[1] - best[0]:
                        best = cand
                    start = i + 1
            if not has_bad:
                return (l, r)
            cand = solve(start, r)
            if cand[1] - cand[0] > best[1] - best[0]:
                best = cand
            return best
        a, b = solve(0, len(s))
        return s[a:b]""",
        "java": """        int[] res = solve(s, 0, s.length());
        return s.substring(res[0], res[1]);
    }
    private int[] solve(String s, int l, int r) {
        if (r - l < 2) return new int[]{0, 0};
        int lower = 0, upper = 0;
        for (int i = l; i < r; i++) {
            char c = s.charAt(i);
            if (c >= 'a') lower |= 1 << (c - 'a');
            else upper |= 1 << (c - 'A');
        }
        int good = lower & upper;
        int start = l;
        int[] best = {0, 0};
        boolean hasBad = false;
        for (int i = l; i < r; i++) {
            char c = s.charAt(i);
            int bit = 1 << (c >= 'a' ? c - 'a' : c - 'A');
            if ((good & bit) == 0) {
                hasBad = true;
                int[] cand = solve(s, start, i);
                if (cand[1] - cand[0] > best[1] - best[0]) best = cand;
                start = i + 1;
            }
        }
        if (!hasBad) return new int[]{l, r};
        int[] cand = solve(s, start, r);
        if (cand[1] - cand[0] > best[1] - best[0]) best = cand;
        return best;""",
        "visible": [{"s": "YazaAay"}, {"s": "Bb"}, {"s": "c"}],
        "hidden": [
            {"s": "dDzeE"},
            {"s": "cChH"},
            {"s": "abABB"},
            {"s": "aAbBcCd"},
            {"s": "xYyXzZz"},
            {"s": "abcdefABCDEF"},
            {"s": "aAbBcXdeDEfF"},
            {"s": "aA" * 200 + "z" + "bB" * 200},
            {"s": "AaBbCcDdEe" * 50},
        ],
    },
    {
        "slug": "81-optimal-partition-of-string",
        "title": "Optimal Partition of String",
        "difficulty": "Medium",
        "subtopic": "Substrings",
        "companies": ["Amazon", "Microsoft", "Google"],
        "desc": "Given a lowercase string `s`, partition `s` into one or more contiguous substrings such that the characters in each substring are all unique (no letter appears more than once within the same substring). Return the minimum number of substrings required in such a partition.",
        "cons": ["1 <= s.length <= 10^5", "s consists of lowercase English letters."],
        "hints": [
            "Greedily extend the current substring as far right as possible while tracking seen characters in a 26-bit mask.",
            "Whenever the next character is already in the current substring's bitmask, start a new substring and reset the bitmask to just that character."
        ],
        "explanations": [
            "\"abacaba\" can be partitioned into [\"ab\", \"ac\", \"ab\", \"a\"] using 4 substrings.",
            "All characters in \"ssssss\" are identical, so each must be in its own substring (6 total).",
            "All characters in \"abcd\" are unique, so 1 substring suffices."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "partitionString",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        parts = 1
        mask = 0
        for ch in s:
            bit = 1 << (ord(ch) - 97)
            if mask & bit:
                parts += 1
                mask = bit
            else:
                mask |= bit
        return parts""",
        "java": """        int parts = 1, mask = 0;
        for (int i = 0; i < s.length(); i++) {
            int bit = 1 << (s.charAt(i) - 'a');
            if ((mask & bit) != 0) {
                parts++;
                mask = bit;
            } else {
                mask |= bit;
            }
        }
        return parts;""",
        "visible": [
            {"s": "abacaba"},
            {"s": "ssssss"},
            {"s": "abcd"},
        ],
        "hidden": [
            {"s": "a"},
            {"s": "aa"},
            {"s": "abca"},
            {"s": "hdklqkcssgxlvehva"},
            {"s": "gizfdfri"},
            {"s": "aabbccdd"},
            {"s": "abcdefghijklmnopqrstuvwxyz"},
            {"s": "abcde" * 200},
            {"s": "a" * 500 + "bcdef" + "a" * 500},
        ],
    },
    {
        "slug": "82-push-dominoes",
        "title": "Push Dominoes",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Google", "Meta", "Amazon"],
        "desc": "There are `n` dominoes in a line, represented by a string `dominoes` where `'L'` means the `i`-th domino was pushed left, `'R'` means it was pushed right, and `'.'` means it was not pushed. Each second, a falling domino pushes its adjacent upright domino in the same direction; a domino pushed equally from both sides simultaneously stays upright. Return the string representing the final state.",
        "cons": ["1 <= dominoes.length <= 10^5", "dominoes[i] is 'L', 'R', or '.'."],
        "hints": [
            "Consider each maximal segment of '.' bounded by non-dot symbols (using virtual 'L' at index -1 and 'R' at index n).",
            "If both boundaries match ('L'..'L' or 'R'..'R'), fill the middle with that symbol; if 'R'..'L', push inward from both ends leaving the exact middle '.' if odd."
        ],
        "explanations": [
            "Each pushed domino knocks over the single adjacent dot until balanced.",
            "Opposing 'R' and 'L' forces meet in the middle, leaving an odd center upright.",
            "No domino is pushed, so all remain upright."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "pushDominoes",
        "params": [("dominoes", "String")],
        "ret": "String",
        "py": """        arr = list(dominoes)
        n = len(arr)
        prev_i = -1
        prev_c = 'L'
        for i in range(n + 1):
            cur_c = arr[i] if i < n else 'R'
            if cur_c == '.':
                continue
            if prev_c == cur_c:
                for k in range(prev_i + 1, i):
                    arr[k] = cur_c
            elif prev_c == 'R' and cur_c == 'L':
                l, r = prev_i + 1, i - 1
                while l < r:
                    arr[l] = 'R'
                    arr[r] = 'L'
                    l += 1
                    r -= 1
            prev_i, prev_c = i, cur_c
        return "".join(arr)""",
        "java": """        char[] arr = dominoes.toCharArray();
        int n = arr.length;
        int prevI = -1;
        char prevC = 'L';
        for (int i = 0; i <= n; i++) {
            char curC = i < n ? arr[i] : 'R';
            if (curC == '.') continue;
            if (prevC == curC) {
                for (int k = prevI + 1; k < i; k++) arr[k] = curC;
            } else if (prevC == 'R' && curC == 'L') {
                int l = prevI + 1, r = i - 1;
                while (l < r) {
                    arr[l++] = 'R';
                    arr[r--] = 'L';
                }
            }
            prevI = i;
            prevC = curC;
        }
        return new String(arr);""",
        "visible": [
            {"dominoes": "RR.L"},
            {"dominoes": ".L.R...LR..L.."},
            {"dominoes": "....."},
        ],
        "hidden": [
            {"dominoes": "."},
            {"dominoes": "L"},
            {"dominoes": "R"},
            {"dominoes": "R....L"},
            {"dominoes": "R...L"},
            {"dominoes": "L...R"},
            {"dominoes": "...L...R..."},
            {"dominoes": "R" + "." * 500 + "L" + "." * 500 + "R"},
            {"dominoes": "R...L." * 200},
        ],
    },
    {
        "slug": "83-shifting-letters",
        "title": "Shifting Letters",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Amazon", "Google", "Bloomberg"],
        "desc": "You are given a lowercase string `s` and an integer array `shifts` of the same length. Shifting a letter moves it forward in the English alphabet cyclically (`'z'` wraps to `'a'`). For each `i` from `0` to `n - 1`, shift the first `i + 1` letters of `s` by `shifts[i]` positions. Return the final string after all shifts are applied.",
        "cons": ["1 <= s.length <= 10^5", "shifts.length == s.length", "0 <= shifts[i] <= 10^9"],
        "hints": [
            "Character s[i] is shifted by the suffix sum shifts[i] + shifts[i + 1] + ... + shifts[n - 1].",
            "Traverse from right to left accumulating the suffix sum modulo 26."
        ],
        "explanations": [
            "Total shifts are [17, 14, 9]: 'a'+17='r', 'b'+14='p', 'c'+9='l'.",
            "Total shifts are [6, 5, 3]: 'a'+6='g', 'a'+5='f', 'a'+3='d'.",
            "Shifting 'z' by 1 wraps around to 'a'."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "shiftingLetters",
        "params": [("s", "String"), ("shifts", "int[]")],
        "ret": "String",
        "py": """        n = len(s)
        chars = list(s)
        acc = 0
        for i in range(n - 1, -1, -1):
            acc = (acc + shifts[i]) % 26
            chars[i] = chr((ord(chars[i]) - 97 + acc) % 26 + 97)
        return "".join(chars)""",
        "java": """        int n = s.length();
        char[] chars = s.toCharArray();
        int acc = 0;
        for (int i = n - 1; i >= 0; i--) {
            acc = (acc + shifts[i] % 26) % 26;
            chars[i] = (char) ('a' + (chars[i] - 'a' + acc) % 26);
        }
        return new String(chars);""",
        "visible": [
            {"s": "abc", "shifts": [3, 5, 9]},
            {"s": "aaa", "shifts": [1, 2, 3]},
            {"s": "z", "shifts": [1]},
        ],
        "hidden": [
            {"s": "a", "shifts": [0]},
            {"s": "a", "shifts": [26]},
            {"s": "xyz", "shifts": [1000000000, 1000000000, 1000000000]},
            {"s": "bad", "shifts": [10, 20, 30]},
            {"s": "ruu", "shifts": [26, 9, 17]},
            {"s": "leetcode", "shifts": [1, 2, 3, 4, 5, 6, 7, 8]},
            {"s": "zzzz", "shifts": [25, 25, 25, 25]},
            {"s": "abcde" * 200, "shifts": [i % 1000 for i in range(1000)]},
            {"s": "m" * 500, "shifts": [1000000000] * 500},
        ],
    },
    {
        "slug": "84-find-and-replace-pattern",
        "title": "Find and Replace Pattern",
        "difficulty": "Medium",
        "subtopic": "String Matching",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": "Given an array of lowercase strings `words` and a lowercase string `pattern`, return a list of all words in `words` (preserving their original order) that match `pattern`. A word matches `pattern` if there exists a bijection (one-to-one and onto mapping) between letters such that replacing every letter `x` in `pattern` with `p(x)` produces the word.",
        "cons": ["1 <= words.length <= 200", "1 <= pattern.length <= 50", "words[i].length == pattern.length", "All characters are lowercase English letters."],
        "hints": [
            "Normalize a string by assigning each newly encountered character its first-seen integer ID (0, 1, 2, ...).",
            "Alternatively check forward and backward 26-element mapping arrays for each word against pattern."
        ],
        "explanations": [
            "\"mee\" and \"aqq\" share the exact (0,1,1) pattern of \"abb\".",
            "Every single-character word matches \"a\".",
            "\"aba\" and \"cdc\" both follow the (0,1,0) pattern of \"xyx\"."
        ],
        "time": "O(N * L)",
        "space": "O(N * L)",
        "method": "findAndReplacePattern",
        "params": [("words", "String[]"), ("pattern", "String")],
        "ret": "List<String>",
        "py": """        def matches(w: str) -> bool:
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
        return [w for w in words if matches(w)]""",
        "java": """        List<String> ans = new ArrayList<>();
        for (String w : words) {
            if (matches(w, pattern)) ans.add(w);
        }
        return ans;
    }
    private boolean matches(String w, String p) {
        int[] p2w = new int[26], w2p = new int[26];
        Arrays.fill(p2w, -1);
        Arrays.fill(w2p, -1);
        for (int i = 0; i < p.length(); i++) {
            int pi = p.charAt(i) - 'a', wi = w.charAt(i) - 'a';
            if (p2w[pi] == -1 && w2p[wi] == -1) {
                p2w[pi] = wi;
                w2p[wi] = pi;
            } else if (p2w[pi] != wi || w2p[wi] != pi) {
                return false;
            }
        }
        return true;""",
        "visible": [
            {"words": ["abc", "deq", "mee", "aqq", "dkd", "ccc"], "pattern": "abb"},
            {"words": ["a", "b", "c"], "pattern": "a"},
            {"words": ["aba", "cdc", "aaa", "abc"], "pattern": "xyx"},
        ],
        "hidden": [
            {"words": ["badc", "abab", "dddd", "dede", "yyxx"], "pattern": "baba"},
            {"words": ["ef", "fq", "ao", "at", "lx"], "pattern": "ya"},
            {"words": ["aaaa", "bbbb", "abbb"], "pattern": "zzzz"},
            {"words": ["abcde", "fghij", "abcda"], "pattern": "vwxyz"},
            {"words": ["paper", "title", "fooaa", "eggss"], "pattern": "title"},
            {"words": ["aa", "ab", "ba", "bb"], "pattern": "cc"},
            {"words": ["no", "match"], "pattern": "aa"},
            {"words": ["abacaba", "xyxzxyx", "abacada", "cdcecdc"], "pattern": "mnmpnmn"},
            {"words": ["aabbc", "ccdde", "abcde", "zzxxq"] * 40, "pattern": "xxyyz"},
        ],
    },
    {
        "slug": "85-camelcase-matching",
        "title": "Camelcase Matching",
        "difficulty": "Medium",
        "subtopic": "String Matching",
        "companies": ["Google", "Microsoft", "Atlassian"],
        "desc": "Given an array of strings `queries` and a string `pattern`, return a boolean array `answer` where `answer[i]` is `true` if `queries[i]` matches `pattern`, and `false` otherwise. A query matches `pattern` if we can insert zero or more lowercase English letters anywhere into `pattern` to obtain the query.",
        "cons": ["1 <= queries.length <= 200", "1 <= queries[i].length, pattern.length <= 100", "queries[i] and pattern consist of uppercase and lowercase English letters."],
        "hints": [
            "Use a two-pointer scan over each query and pattern.",
            "Advance the pattern pointer when characters match; otherwise the query character must be lowercase, or matching immediately fails."
        ],
        "explanations": [
            "\"FooBar\" and \"FooBarTest\" match \"FB\", whereas \"FootBall\" and \"ForceFeedBack\" contain extra uppercase letters or mismatch.",
            "Inserting lowercase letters into \"FoBa\" forms \"FooBar\" and \"FootBall\" only.",
            "\"FooBarTest\" matches \"FoBaT\", while the other queries lack the uppercase 'T'."
        ],
        "time": "O(sum(|queries[i]|))",
        "space": "O(queries.length)",
        "method": "camelMatch",
        "params": [("queries", "String[]"), ("pattern", "String")],
        "ret": "boolean[]",
        "py": """        def ok(q: str) -> bool:
            j = 0
            m = len(pattern)
            for ch in q:
                if j < m and ch == pattern[j]:
                    j += 1
                elif 'A' <= ch <= 'Z':
                    return False
            return j == m
        return [ok(q) for q in queries]""",
        "java": """        boolean[] ans = new boolean[queries.length];
        for (int k = 0; k < queries.length; k++) {
            String q = queries[k];
            int j = 0, m = pattern.length();
            boolean valid = true;
            for (int i = 0; i < q.length(); i++) {
                char c = q.charAt(i);
                if (j < m && c == pattern.charAt(j)) j++;
                else if (c >= 'A' && c <= 'Z') { valid = false; break; }
            }
            ans[k] = valid && j == m;
        }
        return ans;""",
        "visible": [
            {"queries": ["FooBar", "FooBarTest", "FootBall", "FrameBuffer", "ForceFeedBack"], "pattern": "FB"},
            {"queries": ["FooBar", "FooBarTest", "FootBall", "FrameBuffer", "ForceFeedBack"], "pattern": "FoBa"},
            {"queries": ["FooBar", "FooBarTest", "FootBall", "FrameBuffer", "ForceFeedBack"], "pattern": "FoBaT"},
        ],
        "hidden": [
            {"queries": ["CompetitiveProgramming", "CounterPick", "ControlPanel"], "pattern": "CooP"},
            {"queries": ["abc", "aBc", "ABC"], "pattern": "abc"},
            {"queries": ["A", "aA", "Aa", "AA"], "pattern": "A"},
            {"queries": ["lowercase", "another"], "pattern": "lc"},
            {"queries": ["CamelCase", "CamelCaseExtra", "camelCase"], "pattern": "CC"},
            {"queries": ["a", "b", "c"], "pattern": "ab"},
            {"queries": ["FooBarBaz"], "pattern": "FBB"},
            {"queries": ["FooBarBaz"], "pattern": "FB"},
            {"queries": ["AlphaBetaGamma", "AlphaBeta", "AlphaBetaGammaDelta"] * 50, "pattern": "ABG"},
        ],
    },
    {
        "slug": "86-number-of-matching-subsequences",
        "title": "Number of Matching Subsequences",
        "difficulty": "Medium",
        "subtopic": "String Matching",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": "Given a lowercase string `s` and an array of lowercase strings `words`, return the number of elements `words[i]` that are subsequences of `s`. Duplicate words in `words` are counted each time they appear if they are subsequences of `s`.",
        "cons": ["1 <= s.length <= 5 * 10^4", "1 <= words.length <= 5000", "1 <= words[i].length <= 50"],
        "hints": [
            "Checking each word against s from scratch takes O(|words| * |s|), which can be too slow.",
            "Group waiting words into 26 buckets keyed by their next needed character, and scan s once advancing only the bucket for s[i]."
        ],
        "explanations": [
            "\"a\", \"acd\", and \"ace\" are subsequences of \"abcde\", while \"bb\" is not.",
            "\"ahjpjau\" and \"ahbwzgqnuk\" are subsequences of `s`, giving count 2.",
            "Duplicate valid words like [\"aa\", \"aa\"] are each counted."
        ],
        "time": "O(|s| + sum(|words[i]|))",
        "space": "O(words.length)",
        "method": "numMatchingSubseq",
        "params": [("s", "String"), ("words", "String[]")],
        "ret": "int",
        "py": """        buckets = [[] for _ in range(26)]
        for w in words:
            buckets[ord(w[0]) - 97].append((w, 0))
        ans = 0
        for ch in s:
            idx = ord(ch) - 97
            cur = buckets[idx]
            buckets[idx] = []
            for w, pos in cur:
                nxt = pos + 1
                if nxt == len(w):
                    ans += 1
                else:
                    buckets[ord(w[nxt]) - 97].append((w, nxt))
        return ans""",
        "java": """        @SuppressWarnings("unchecked")
        List<int[]>[] buckets = new ArrayList[26];
        for (int i = 0; i < 26; i++) buckets[i] = new ArrayList<>();
        for (int i = 0; i < words.length; i++) {
            buckets[words[i].charAt(0) - 'a'].add(new int[]{i, 0});
        }
        int ans = 0;
        for (int i = 0; i < s.length(); i++) {
            int idx = s.charAt(i) - 'a';
            List<int[]> cur = buckets[idx];
            buckets[idx] = new ArrayList<>();
            for (int[] pair : cur) {
                int wi = pair[0], pos = pair[1] + 1;
                if (pos == words[wi].length()) ans++;
                else buckets[words[wi].charAt(pos) - 'a'].add(new int[]{wi, pos});
            }
        }
        return ans;""",
        "visible": [
            {"s": "abcde", "words": ["a", "bb", "acd", "ace"]},
            {"s": "dsahjpjauf", "words": ["ahjpjau", "ja", "ahbwzgqnuk", "tnmlanowax"]},
            {"s": "aaa", "words": ["aa", "aa", "aaaa"]},
        ],
        "hidden": [
            {"s": "a", "words": ["a", "b"]},
            {"s": "abcdef", "words": ["fed", "ace", "bdf", "abcdef", "abcdefg"]},
            {"s": "xyz", "words": ["x", "y", "z", "xy", "xz", "yz", "xyz"]},
            {"s": "abacaba", "words": ["aaa", "aba", "cab", "bbb", "abca"]},
            {"s": "zzzz", "words": ["z", "zz", "zzz", "zzzz", "zzzzz"]},
            {"s": "qlhxagxdqh", "words": ["qlhxagxdq", "qlhxagxdq", "lhyiftwtut", "yfzwraahab"]},
            {"s": "abcdefghijklmnopqrstuvwxyz", "words": ["acegikmoqsuwy", "zyx", "amz", "mnop"]},
            {"s": "abcde" * 400, "words": ["abcde" * 5, "edcba", "aaaaa", "zzzzz"] * 50},
            {"s": "a" * 2000 + "b", "words": ["a" * 40 + "b", "b" + "a"] * 100},
        ],
    },
    {
        "slug": "87-shortest-way-to-form-string",
        "title": "Shortest Way to Form String",
        "difficulty": "Medium",
        "subtopic": "String Matching",
        "companies": ["Google", "Meta", "Amazon"],
        "desc": "Given two lowercase strings `source` and `target`, return the minimum number of subsequences of `source` such that their concatenation equals `target`. If `target` cannot be formed this way, return `-1`.",
        "cons": ["1 <= source.length, target.length <= 10^4", "source and target consist of lowercase English letters."],
        "hints": [
            "If target contains any character that never appears in source, return -1 immediately.",
            "Precompute nextPos[i][c]: the earliest index >= i in source where character c occurs (or -1). Greedily match as many target characters as possible in each pass over source."
        ],
        "explanations": [
            "\"abcbc\" can be formed as \"ab\" + \"cbc\" (2 subsequences of \"abc\").",
            "'d' does not appear in \"abc\", so return -1.",
            "\"xzyxz\" = \"xz\" + \"y\" + \"xz\" (3 subsequences of \"xyz\")."
        ],
        "time": "O(26 * |source| + |target|)",
        "space": "O(26 * |source|)",
        "method": "shortestWay",
        "params": [("source", "String"), ("target", "String")],
        "ret": "int",
        "py": """        m = len(source)
        nxt = [[-1] * 26 for _ in range(m + 1)]
        for i in range(m - 1, -1, -1):
            nxt[i] = nxt[i + 1][:]
            nxt[i][ord(source[i]) - 97] = i
        ans = 1
        pos = 0
        for ch in target:
            c = ord(ch) - 97
            if nxt[0][c] == -1:
                return -1
            if nxt[pos][c] == -1:
                ans += 1
                pos = 0
            pos = nxt[pos][c] + 1
        return ans""",
        "java": """        int m = source.length();
        int[][] nxt = new int[m + 1][26];
        Arrays.fill(nxt[m], -1);
        for (int i = m - 1; i >= 0; i--) {
            System.arraycopy(nxt[i + 1], 0, nxt[i], 0, 26);
            nxt[i][source.charAt(i) - 'a'] = i;
        }
        int ans = 1, pos = 0;
        for (int i = 0; i < target.length(); i++) {
            int c = target.charAt(i) - 'a';
            if (nxt[0][c] == -1) return -1;
            if (nxt[pos][c] == -1) {
                ans++;
                pos = 0;
            }
            pos = nxt[pos][c] + 1;
        }
        return ans;""",
        "visible": [
            {"source": "abc", "target": "abcbc"},
            {"source": "abc", "target": "acdbc"},
            {"source": "xyz", "target": "xzyxz"},
        ],
        "hidden": [
            {"source": "a", "target": "a"},
            {"source": "a", "target": "aaaaa"},
            {"source": "a", "target": "b"},
            {"source": "aaaaa", "target": "aaaaaaaaaaaaa"},
            {"source": "abcde", "target": "edcba"},
            {"source": "abcab", "target": "aabbaac"},
            {"source": "abcdef", "target": "abcdef"},
            {"source": "abcdefghij", "target": "jihgfedcba" * 50},
            {"source": "abcde" * 20, "target": "edcba" * 100},
        ],
    },
    {
        "slug": "88-longest-word-in-dictionary-through-deleting",
        "title": "Longest Word in Dictionary through Deleting",
        "difficulty": "Medium",
        "subtopic": "String Matching",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": "Given a lowercase string `s` and an array of lowercase strings `dictionary`, return the longest string in `dictionary` that can be formed by deleting zero or more characters from `s` (i.e., is a subsequence of `s`). If multiple words tie for the longest length, return the lexicographically smallest one; if none qualify, return `\"\"`.",
        "cons": ["1 <= s.length <= 1000", "1 <= dictionary.length <= 1000", "1 <= dictionary[i].length <= 1000"],
        "hints": [
            "You can test whether word w is a subsequence of s in O(|s|) time with a two-pointer scan.",
            "Only run the subsequence check if w is strictly better than the current best answer (longer, or equal length and lexicographically smaller)."
        ],
        "explanations": [
            "\"ale\", \"apple\", and \"plea\" are subsequences of \"abpcplea\", and \"apple\" is the longest (length 5).",
            "\"a\", \"b\", and \"c\" all have length 1; \"a\" is lexicographically smallest.",
            "No dictionary word is a subsequence of \"xyz\", so return \"\"."
        ],
        "time": "O(sum(|s|))",
        "space": "O(1)",
        "method": "findLongestWord",
        "params": [("s", "String"), ("dictionary", "String[]")],
        "ret": "String",
        "py": """        best = ""
        n = len(s)
        for w in dictionary:
            if len(w) < len(best) or (len(w) == len(best) and w >= best):
                continue
            i = j = 0
            m = len(w)
            while i < n and j < m:
                if s[i] == w[j]:
                    j += 1
                i += 1
            if j == m:
                best = w
        return best""",
        "java": """        String best = "";
        int n = s.length();
        for (String w : dictionary) {
            if (w.length() < best.length() || (w.length() == best.length() && w.compareTo(best) >= 0)) {
                continue;
            }
            int i = 0, j = 0, m = w.length();
            while (i < n && j < m) {
                if (s.charAt(i) == w.charAt(j)) j++;
                i++;
            }
            if (j == m) best = w;
        }
        return best;""",
        "visible": [
            {"s": "abpcplea", "dictionary": ["ale", "apple", "monkey", "plea"]},
            {"s": "abpcplea", "dictionary": ["a", "b", "c"]},
            {"s": "xyz", "dictionary": ["abc", "def"]},
        ],
        "hidden": [
            {"s": "a", "dictionary": ["a"]},
            {"s": "bab", "dictionary": ["ba", "ab", "a", "b"]},
            {"s": "abce", "dictionary": ["abe", "abc"]},
            {"s": "wordgoodgoodgoodbestword", "dictionary": ["word", "good", "best", "goodbest"]},
            {"s": "aaa", "dictionary": ["aaa", "aa", "a"]},
            {"s": "abcdefg", "dictionary": ["gfedcba", "aceg", "bdf", "abef"]},
            {"s": "mississippi", "dictionary": ["misp", "miss", "ssippi", "issppi"]},
            {"s": "abcdefghijklmnopqrstuvwxyz", "dictionary": ["acegik", "bdfhjl", "abcxyz", "mnopqr"]},
            {"s": "abcde" * 100, "dictionary": ["a" * 50, "e" * 50, "abcde" * 20, "edcba" * 10]},
        ],
    },
    {
        "slug": "89-minimum-window-subsequence",
        "title": "Minimum Window Subsequence",
        "difficulty": "Hard",
        "subtopic": "Substrings",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": "Given lowercase strings `s1` and `s2`, return the shortest contiguous substring `w` of `s1` such that `s2` is a subsequence of `w`. If there is no such substring, return `\"\"`. If multiple substrings have the same minimum length, return the one with the smallest starting index.",
        "cons": ["1 <= s1.length <= 2 * 10^4", "1 <= s2.length <= 100", "s1 and s2 consist of lowercase English letters."],
        "hints": [
            "Scan forward in s1 to find the end of a match for s2, then scan backward from that endpoint to shrink the window to the tightest possible start index.",
            "After finding a minimal window [start, end], resume the next forward search from start + 1 (or use DP tracking the latest valid start index for each prefix of s2)."
        ],
        "explanations": [
            "\"bcde\" is the shortest substring of \"abcdebdde\" containing \"bde\" as a subsequence.",
            "\"mccqouqadqtm\" is the shortest substring containing \"mm\" as a subsequence.",
            "\"abcdef\" does not contain \"u\", so return \"\"."
        ],
        "time": "O(|s1| * |s2|)",
        "space": "O(1)",
        "method": "minWindowSubsequence",
        "params": [("s1", "String"), ("s2", "String")],
        "ret": "String",
        "py": """        n, m = len(s1), len(s2)
        best_start = -1
        best_len = n + 1
        i = 0
        while i < n:
            j = 0
            while i < n:
                if s1[i] == s2[j]:
                    j += 1
                    if j == m:
                        break
                i += 1
            if j < m:
                break
            end = i
            j = m - 1
            while j >= 0:
                if s1[i] == s2[j]:
                    j -= 1
                i -= 1
            start = i + 1
            if end - start + 1 < best_len:
                best_len = end - start + 1
                best_start = start
            i = start + 1
        return "" if best_start == -1 else s1[best_start:best_start + best_len]""",
        "java": """        int n = s1.length(), m = s2.length();
        int bestStart = -1, bestLen = n + 1;
        int i = 0;
        while (i < n) {
            int j = 0;
            while (i < n) {
                if (s1.charAt(i) == s2.charAt(j)) {
                    j++;
                    if (j == m) break;
                }
                i++;
            }
            if (j < m) break;
            int end = i;
            j = m - 1;
            while (j >= 0) {
                if (s1.charAt(i) == s2.charAt(j)) j--;
                i--;
            }
            int start = i + 1;
            if (end - start + 1 < bestLen) {
                bestLen = end - start + 1;
                bestStart = start;
            }
            i = start + 1;
        }
        return bestStart == -1 ? "" : s1.substring(bestStart, bestStart + bestLen);""",
        "visible": [
            {"s1": "abcdebdde", "s2": "bde"},
            {"s1": "cnhczmccqouqadqtmjjzl", "s2": "mm"},
            {"s1": "abcdef", "s2": "u"},
        ],
        "hidden": [
            {"s1": "a", "s2": "a"},
            {"s1": "a", "s2": "aa"},
            {"s1": "fgrqsqsnodwmxzkzxwqegkndaa", "s2": "fnok"},
            {"s1": "abacabadabacaba", "s2": "aba"},
            {"s1": "xabxaxb", "s2": "ab"},
            {"s1": "abcdeabcde", "s2": "ace"},
            {"s1": "bbbaaabbb", "s2": "bab"},
            {"s1": "ab" * 300 + "cde" + "ab" * 300, "s2": "acde"},
            {"s1": "a" * 500 + "b" + "a" * 10 + "c" + "a" * 500, "s2": "abc"},
        ],
    },
    {
        "slug": "90-orderly-queue",
        "title": "Orderly Queue",
        "difficulty": "Hard",
        "subtopic": "String Matching",
        "companies": ["Google", "Amazon", "Microsoft"],
        "desc": "You are given a lowercase string `s` and an integer `k`. In one move, you may pick any one of the first `k` characters of `s` and append it to the end of `s`. Return the lexicographically smallest string achievable after applying any number of moves.",
        "cons": ["1 <= k <= s.length <= 1000", "s consists of lowercase English letters."],
        "hints": [
            "When k == 1, you can only rotate the string cyclically, so return the lexicographically smallest rotation.",
            "When k >= 2, you can swap any two adjacent characters (bubble sort), which means any permutation is reachable—simply sort s."
        ],
        "explanations": [
            "With k = 1, the rotations of \"cba\" are \"cba\", \"bac\", and \"acb\"; \"acb\" is smallest.",
            "With k = 3 (>= 2), any permutation is reachable, so sorting gives \"aaabc\".",
            "With k = 2, sorting \"dcba\" produces \"abcd\"."
        ],
        "time": "O(n^2) for k=1, O(n log n) for k>=2",
        "space": "O(n)",
        "method": "orderlyQueue",
        "params": [("s", "String"), ("k", "int")],
        "ret": "String",
        "py": """        if k == 1:
            return min(s[i:] + s[:i] for i in range(len(s)))
        return "".join(sorted(s))""",
        "java": """        if (k == 1) {
            String best = s;
            for (int i = 1; i < s.length(); i++) {
                String cand = s.substring(i) + s.substring(0, i);
                if (cand.compareTo(best) < 0) best = cand;
            }
            return best;
        }
        char[] arr = s.toCharArray();
        Arrays.sort(arr);
        return new String(arr);""",
        "visible": [
            {"s": "cba", "k": 1},
            {"s": "baaca", "k": 3},
            {"s": "dcba", "k": 2},
        ],
        "hidden": [
            {"s": "a", "k": 1},
            {"s": "zxy", "k": 1},
            {"s": "ababab", "k": 1},
            {"s": "nhtq", "k": 1},
            {"s": "gfedcba", "k": 2},
            {"s": "leetcode", "k": 1},
            {"s": "leetcode", "k": 2},
            {"s": "zyxwvutsrqponmlkjihgfedcba" * 10, "k": 1},
            {"s": "zyxwvutsrqponmlkjihgfedcba" * 10, "k": 2},
        ],
    },
    {
        "slug": "91-check-if-string-is-pangram",
        "title": "Check if the Sentence Is Pangram",
        "difficulty": "Easy",
        "subtopic": "Anagrams",
        "companies": ["Amazon", "Apple", "Adobe"],
        "desc": "A pangram is a sentence in which every letter of the English alphabet (`'a'` through `'z'`) appears at least once. Given a lowercase string `sentence`, return `true` if `sentence` is a pangram, and `false` otherwise.",
        "cons": ["1 <= sentence.length <= 10^4", "sentence consists of lowercase English letters."],
        "hints": [
            "Track seen letters using a 26-bit integer bitmask.",
            "Return true as soon as the mask equals (1 << 26) - 1."
        ],
        "explanations": [
            "\"thequickbrownfoxjumpsoverthelazydog\" contains all 26 letters.",
            "\"leetcode\" is missing most letters of the alphabet.",
            "\"abcdefghijklmnopqrstuvwxyz\" has every letter exactly once."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "checkIfPangram",
        "params": [("sentence", "String")],
        "ret": "boolean",
        "py": """        mask = 0
        full = (1 << 26) - 1
        for ch in sentence:
            mask |= 1 << (ord(ch) - 97)
            if mask == full:
                return True
        return False""",
        "java": """        int mask = 0, full = (1 << 26) - 1;
        for (int i = 0; i < sentence.length(); i++) {
            mask |= 1 << (sentence.charAt(i) - 'a');
            if (mask == full) return true;
        }
        return false;""",
        "visible": [
            {"sentence": "thequickbrownfoxjumpsoverthelazydog"},
            {"sentence": "leetcode"},
            {"sentence": "abcdefghijklmnopqrstuvwxyz"},
        ],
        "hidden": [
            {"sentence": "a"},
            {"sentence": "abcdefghijklmnopqrstuvwxy"},
            {"sentence": "bcdefghijklmnopqrstuvwxyz"},
            {"sentence": "packmyboxwithfivedozenliquorjugs"},
            {"sentence": "sphinxofblackquartzjudgemyvow"},
            {"sentence": "a" * 100},
            {"sentence": "zyxwvutsrqponmlkjihgfedcba"},
            {"sentence": "abcdefghijklm" * 100},
            {"sentence": "a" * 500 + "bcdefghijklmnopqrstuvwxyz"},
        ],
    },
    {
        "slug": "92-jewels-and-stones",
        "title": "Jewels and Stones",
        "difficulty": "Easy",
        "subtopic": "String Matching",
        "companies": ["Amazon", "Google", "Apple"],
        "desc": "You are given two strings: `jewels` representing the distinct types of stones that are jewels, and `stones` representing the stones you have. Letters are case-sensitive (`'a'` and `'A'` are different types). Return how many characters in `stones` are also present in `jewels`.",
        "cons": ["1 <= jewels.length, stones.length <= 10^4", "jewels and stones consist of English letters.", "All characters in jewels are unique."],
        "hints": [
            "Store all characters of jewels in a fast lookup structure (a 128-element boolean array or hash set).",
            "Count how many characters of stones are marked in the lookup table."
        ],
        "explanations": [
            "One 'a' and two 'A's appear in \"aAAbbbb\", totaling 3.",
            "Lowercase 'z' does not match uppercase 'Z', so 0.",
            "Every stone in \"abcABC\" is a jewel."
        ],
        "time": "O(|jewels| + |stones|)",
        "space": "O(1)",
        "method": "numJewelsInStones",
        "params": [("jewels", "String"), ("stones", "String")],
        "ret": "int",
        "py": """        jset = set(jewels)
        return sum(1 for ch in stones if ch in jset)""",
        "java": """        boolean[] isJewel = new boolean[128];
        for (int i = 0; i < jewels.length(); i++) isJewel[jewels.charAt(i)] = true;
        int ans = 0;
        for (int i = 0; i < stones.length(); i++) if (isJewel[stones.charAt(i)]) ans++;
        return ans;""",
        "visible": [
            {"jewels": "aA", "stones": "aAAbbbb"},
            {"jewels": "z", "stones": "ZZ"},
            {"jewels": "abcABC", "stones": "abcABC"},
        ],
        "hidden": [
            {"jewels": "a", "stones": "a"},
            {"jewels": "a", "stones": "b"},
            {"jewels": "bcd", "stones": "cba"},
            {"jewels": "XYZ", "stones": "xyzXYZxyz"},
            {"jewels": "abcdefghijklmnopqrstuvwxyz", "stones": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
            {"jewels": "aeiouAEIOU", "stones": "HelloWorldAlgoPlay"},
            {"jewels": "q", "stones": "qqqqqqqqqq"},
            {"jewels": "aAbBcC", "stones": "aAbBcCdDeEfF" * 200},
            {"jewels": "Z", "stones": "z" * 1000 + "Z" * 250},
        ],
    },
    {
        "slug": "93-uncommon-words-from-two-sentences",
        "title": "Uncommon Words from Two Sentences",
        "difficulty": "Easy",
        "subtopic": "Parsing",
        "companies": ["Amazon", "Meta", "Microsoft"],
        "desc": "A sentence is a string of single-space-separated lowercase words. A word is uncommon if it appears exactly once in one of the sentences and does not appear at all in the other sentence. Given two sentences `s1` and `s2`, return a list of all uncommon words in any order.",
        "cons": ["1 <= s1.length, s2.length <= 10^4", "s1 and s2 consist of lowercase English letters and single spaces separating words."],
        "hints": [
            "A word is uncommon iff its combined frequency across both s1 and s2 equals 1.",
            "Count all words from s1 and s2 in a single hash map and collect those with count == 1."
        ],
        "explanations": [
            "\"sweet\" and \"sour\" each appear once across both sentences.",
            "\"apple\" appears twice in s1, so only \"banana\" is uncommon.",
            "Every word appears twice, so no word is uncommon."
        ],
        "time": "O(|s1| + |s2|)",
        "space": "O(|s1| + |s2|)",
        "compare": "sorted",
        "method": "uncommonFromSentences",
        "params": [("s1", "String"), ("s2", "String")],
        "ret": "String[]",
        "py": """        cnt = Counter(s1.split())
        cnt.update(s2.split())
        return [w for w, c in cnt.items() if c == 1]""",
        "java": """        Map<String, Integer> cnt = new HashMap<>();
        for (String w : s1.split(" ")) cnt.put(w, cnt.getOrDefault(w, 0) + 1);
        for (String w : s2.split(" ")) cnt.put(w, cnt.getOrDefault(w, 0) + 1);
        List<String> out = new ArrayList<>();
        for (Map.Entry<String, Integer> e : cnt.entrySet()) {
            if (e.getValue() == 1) out.add(e.getKey());
        }
        return out.toArray(new String[0]);""",
        "visible": [
            {"s1": "this apple is sweet", "s2": "this apple is sour"},
            {"s1": "apple apple", "s2": "banana"},
            {"s1": "same words", "s2": "same words"},
        ],
        "hidden": [
            {"s1": "a", "s2": "b"},
            {"s1": "a", "s2": "a"},
            {"s1": "s z z z s", "s2": "s z ejt"},
            {"s1": "one two three", "s2": "four five six"},
            {"s1": "foo bar baz foo", "s2": "bar qux quux"},
            {"s1": "x x x", "s2": "y y y"},
            {"s1": "cat dog bird", "s2": "dog fish cat"},
            {"s1": " ".join(f"w{i}" for i in range(100)), "s2": " ".join(f"w{i}" for i in range(50, 150))},
            {"s1": "repeat " * 50 + "uniqueone", "s2": "repeat " * 50 + "uniquetwo"},
        ],
    },
    {
        "slug": "94-unique-email-addresses",
        "title": "Unique Email Addresses",
        "difficulty": "Easy",
        "subtopic": "Parsing",
        "companies": ["Google", "Amazon", "Adobe"],
        "desc": "Every valid email address consists of a local name and a domain name separated by `'@'`. In the local name, periods `'.'` are ignored, and everything from the first `'+'` onward is ignored (these rules do not apply to the domain name). Given an array of valid email strings `emails`, return the number of distinct canonical addresses that actually receive mail.",
        "cons": ["1 <= emails.length <= 500", "1 <= emails[i].length <= 100", "Each email contains exactly one '@' with non-empty local and domain parts."],
        "hints": [
            "Split each email at '@': keep the domain verbatim.",
            "In the local part, truncate at the first '+' (if any), remove all '.', then insert local + '@' + domain into a set."
        ],
        "explanations": [
            "The first two emails normalize to \"testemail@leetcode.com\" and the third to \"testemail@lee.tcode.com\", giving 2 unique addresses.",
            "All three addresses have different local names, giving 3.",
            "Dots and plus-tags in the local name normalize all three to \"user@domain.com\"."
        ],
        "time": "O(sum(|emails[i]|))",
        "space": "O(sum(|emails[i]|))",
        "method": "numUniqueEmails",
        "params": [("emails", "String[]")],
        "ret": "int",
        "py": """        seen = set()
        for e in emails:
            local, domain = e.split('@', 1)
            plus = local.find('+')
            if plus != -1:
                local = local[:plus]
            seen.add(local.replace('.', '') + '@' + domain)
        return len(seen)""",
        "java": """        Set<String> seen = new HashSet<>();
        for (String e : emails) {
            int at = e.indexOf('@');
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < at; i++) {
                char c = e.charAt(i);
                if (c == '+') break;
                if (c != '.') sb.append(c);
            }
            sb.append(e, at, e.length());
            seen.add(sb.toString());
        }
        return seen.size();""",
        "visible": [
            {"emails": ["test.email+alex@leetcode.com", "test.e.mail+bob.cathy@leetcode.com", "testemail+david@lee.tcode.com"]},
            {"emails": ["a@leetcode.com", "b@leetcode.com", "c@leetcode.com"]},
            {"emails": ["u.s.e.r@domain.com", "user+tag@domain.com", "u.ser+1+2@domain.com"]},
        ],
        "hidden": [
            {"emails": ["a@b.com"]},
            {"emails": ["a.b@c.com", "ab@c.com"]},
            {"emails": ["a+b@c.com", "a+d@c.com", "a@c.com"]},
            {"emails": ["x@a.b.com", "x@ab.com"]},
            {"emails": ["test.email+alex@leetcode.com", "test.email.leet+alex@code.com"]},
            {"emails": ["+abc@x.com", "+def@x.com"]},
            {"emails": ["a...b...c+xyz@mail.org", "abc@mail.org", "abc@mail.com"]},
            {"emails": [f"u.s.e.r.{i % 20}+tag{i}@example.com" for i in range(200)]},
            {"emails": [f"user{i}@d{i % 10}.com" for i in range(150)]},
        ],
    },
    {
        "slug": "95-longest-common-substring-length",
        "title": "Longest Common Substring Length",
        "difficulty": "Medium",
        "subtopic": "Substrings",
        "companies": ["Amazon", "Microsoft", "Google"],
        "desc": "Given two lowercase strings `s1` and `s2`, return the length of the longest contiguous substring that appears in both `s1` and `s2`. Return `0` if they share no common character.",
        "cons": ["0 <= s1.length, s2.length <= 1000", "s1 and s2 consist of lowercase English letters."],
        "hints": [
            "Let dp[i][j] be the length of the longest common suffix of s1[:i] and s2[:j].",
            "If s1[i - 1] == s2[j - 1], dp[i][j] = dp[i - 1][j - 1] + 1; otherwise 0. Optimize to O(min(|s1|, |s2|)) space by iterating j backward."
        ],
        "explanations": [
            "\"abcd\" is the longest common contiguous substring of \"abcdxyz\" and \"xyzabcd\", with length 4.",
            "\"bc\" has length 2.",
            "No characters overlap between \"abc\" and \"def\"."
        ],
        "time": "O(|s1| * |s2|)",
        "space": "O(|s2|)",
        "method": "longestCommonSubstring",
        "params": [("s1", "String"), ("s2", "String")],
        "ret": "int",
        "py": """        m = len(s2)
        dp = [0] * (m + 1)
        best = 0
        for ch in s1:
            for j in range(m, 0, -1):
                if ch == s2[j - 1]:
                    dp[j] = dp[j - 1] + 1
                    if dp[j] > best:
                        best = dp[j]
                else:
                    dp[j] = 0
        return best""",
        "java": """        int m = s2.length();
        int[] dp = new int[m + 1];
        int best = 0;
        for (int i = 0; i < s1.length(); i++) {
            char ch = s1.charAt(i);
            for (int j = m; j >= 1; j--) {
                if (ch == s2.charAt(j - 1)) {
                    dp[j] = dp[j - 1] + 1;
                    if (dp[j] > best) best = dp[j];
                } else {
                    dp[j] = 0;
                }
            }
        }
        return best;""",
        "visible": [
            {"s1": "abcdxyz", "s2": "xyzabcd"},
            {"s1": "abcb", "s2": "dbca"},
            {"s1": "abc", "s2": "def"},
        ],
        "hidden": [
            {"s1": "", "s2": "abc"},
            {"s1": "a", "s2": "a"},
            {"s1": "abcdef", "s2": "abcdef"},
            {"s1": "zxabcdezy", "s2": "yzabcdezx"},
            {"s1": "aaaa", "s2": "aaaaaa"},
            {"s1": "mississippi", "s2": "ssip"},
            {"s1": "banana", "s2": "ananas"},
            {"s1": "abacaba" * 30, "s2": "cababac" * 30},
            {"s1": "a" * 200 + "xyz" + "b" * 200, "s2": "c" * 200 + "xyz" + "d" * 200},
        ],
    },
    {
        "slug": "96-minimum-add-to-make-parentheses-valid",
        "title": "Minimum Add to Make Parentheses Valid",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Meta", "Amazon", "Bloomberg"],
        "desc": "A parentheses string is valid if it is empty or can be built from balanced pairs of `'('` and `')'`. Given a string `s` consisting only of `'('` and `')'`, return the minimum number of parentheses you must insert at any positions to make `s` valid.",
        "cons": ["0 <= s.length <= 10^5", "s consists only of '(' and ')'."],
        "hints": [
            "Track the count of currently unmatched '(' (openCount) and unmatched ')' (adds).",
            "When you see ')', decrement openCount if positive, otherwise increment adds; at the end return adds + openCount."
        ],
        "explanations": [
            "Insert one '(' at the start of \"())\" to form \"(())\".",
            "Insert three ')' at the end of \"(((\" to form \"((()))\".",
            "\"()\" is already valid, requiring 0 insertions."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "minAddToMakeValid",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        open_cnt = 0
        adds = 0
        for ch in s:
            if ch == '(':
                open_cnt += 1
            elif open_cnt > 0:
                open_cnt -= 1
            else:
                adds += 1
        return adds + open_cnt""",
        "java": """        int open = 0, adds = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') open++;
            else if (open > 0) open--;
            else adds++;
        }
        return adds + open;""",
        "visible": [{"s": "())"}, {"s": "((("}, {"s": "()"}],
        "hidden": [
            {"s": ""},
            {"s": "("},
            {"s": ")"},
            {"s": "()))(("},
            {"s": "()()()"},
            {"s": "((()))"},
            {"s": ")))((("},
            {"s": ")(" * 500},
            {"s": "(" * 1000 + ")" * 400},
        ],
    },
    {
        "slug": "97-minimum-swaps-to-make-strings-equal",
        "title": "Minimum Swaps to Make Strings Equal",
        "difficulty": "Medium",
        "subtopic": "Anagrams",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs"],
        "desc": "You are given two equal-length strings `s1` and `s2` containing only the characters `'x'` and `'y'`. In one swap, you may choose any index `i` in `s1` and any index `j` in `s2` (possibly `i == j`) and swap `s1[i]` with `s2[j]`. Return the minimum number of swaps required to make `s1` and `s2` equal, or `-1` if it is impossible.",
        "cons": ["1 <= s1.length <= 10^4", "s1.length == s2.length", "s1 and s2 contain only 'x' and 'y'."],
        "hints": [
            "Ignore positions where s1[i] == s2[i]. Count mismatches of type ('x','y') as xy and ('y','x') as yx.",
            "If (xy + yx) is odd it is impossible; otherwise pairs of the same mismatch type cost 1 swap each, and one leftover xy + one leftover yx cost 2 swaps."
        ],
        "explanations": [
            "Swap s1[0] with s2[1] to turn \"xx\" and \"yy\" into \"yx\" and \"yx\" (1 swap).",
            "One ('x','y') and one ('y','x') mismatch require 2 swaps.",
            "Total mismatches is 1 (odd), so making them equal is impossible."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "minimumSwap",
        "params": [("s1", "String"), ("s2", "String")],
        "ret": "int",
        "py": """        xy = yx = 0
        for a, b in zip(s1, s2):
            if a == 'x' and b == 'y':
                xy += 1
            elif a == 'y' and b == 'x':
                yx += 1
        if (xy + yx) & 1:
            return -1
        return xy // 2 + yx // 2 + (xy & 1) * 2""",
        "java": """        int xy = 0, yx = 0;
        for (int i = 0; i < s1.length(); i++) {
            char a = s1.charAt(i), b = s2.charAt(i);
            if (a == 'x' && b == 'y') xy++;
            else if (a == 'y' && b == 'x') yx++;
        }
        if (((xy + yx) & 1) == 1) return -1;
        return xy / 2 + yx / 2 + (xy & 1) * 2;""",
        "visible": [
            {"s1": "xx", "s2": "yy"},
            {"s1": "xy", "s2": "yx"},
            {"s1": "xx", "s2": "xy"},
        ],
        "hidden": [
            {"s1": "x", "s2": "x"},
            {"s1": "x", "s2": "y"},
            {"s1": "xxyyxyxyxx", "s2": "xyyxyxxxyx"},
            {"s1": "xyxy", "s2": "yxyx"},
            {"s1": "xxxx", "s2": "yyyy"},
            {"s1": "xyxyx", "s2": "yxyxy"},
            {"s1": "yyyxxx", "s2": "yyyxxx"},
            {"s1": "xy" * 500, "s2": "yx" * 500},
            {"s1": "x" * 501 + "y" * 499, "s2": "y" * 501 + "x" * 499},
        ],
    },
    {
        "slug": "98-minimum-swaps-to-make-brackets-balanced",
        "title": "Minimum Number of Swaps to Make the String Balanced",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Meta", "Amazon", "Google"],
        "desc": "You are given a 0-indexed even-length string `s` consisting of exactly `n / 2` opening brackets `'['` and `n / 2` closing brackets `']'`. In one swap, you may swap characters at any two indices. Return the minimum number of swaps needed to make `s` a balanced bracket string.",
        "cons": ["2 <= s.length <= 10^5", "s.length is even and contains equal numbers of '[' and ']'."],
        "hints": [
            "Track the maximum imbalance (the peak excess of ']' over '[' seen at any prefix).",
            "Each optimal swap fixes two units of imbalance, so the answer is (maxImbalance + 1) // 2."
        ],
        "explanations": [
            "Swapping index 0 and index 3 turns \"][][\" into \"[[]]\" in 1 swap.",
            "Maximum excess of ']' is 3, requiring (3 + 1) // 2 = 2 swaps.",
            "\"[]\" is already balanced, needing 0 swaps."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "minSwapsBalanced",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        close = 0
        max_close = 0
        for ch in s:
            if ch == '[':
                close -= 1
            else:
                close += 1
                if close > max_close:
                    max_close = close
        return (max_close + 1) // 2""",
        "java": """        int close = 0, maxClose = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '[') close--;
            else {
                close++;
                if (close > maxClose) maxClose = close;
            }
        }
        return (maxClose + 1) / 2;""",
        "visible": [{"s": "][]["}, {"s": "]]][[["}, {"s": "[]"}],
        "hidden": [
            {"s": "]["},
            {"s": "[[]]"},
            {"s": "[]][[]"},
            {"s": "]]]][[[["},
            {"s": "][][][]["},
            {"s": "]][][[[" + "]"},
            {"s": "[][][][]"},
            {"s": "]" * 500 + "[" * 500},
            {"s": "][" * 500},
        ],
    },
    {
        "slug": "99-distinct-echo-substrings",
        "title": "Distinct Echo Substrings",
        "difficulty": "Hard",
        "subtopic": "String Matching",
        "companies": ["Google", "Meta", "Uber"],
        "desc": "Return the number of distinct non-empty contiguous substrings of `text` that can be written as the concatenation of some string with itself (i.e., of the form `a + a` where `a` is non-empty).",
        "cons": ["1 <= text.length <= 2000", "text consists of lowercase English letters."],
        "hints": [
            "Precompute polynomial rolling hashes (or 64-bit / double hashes) so any two substrings can be compared in O(1).",
            "For each even half-length L from 1 to n // 2, slide across indices i checking if hash(i, i + L) == hash(i + L, i + 2*L) and store matching hashes in a set."
        ],
        "explanations": [
            "The 3 distinct echo substrings of \"abcabcabc\" are \"abcabc\", \"bcabca\", and \"cabcab\".",
            "The 2 distinct echo substrings of \"leetcodeleetcode\" are \"ee\" and \"leetcodeleetcode\".",
            "\"aaaa\" has 2 distinct echo substrings: \"aa\" and \"aaaa\"."
        ],
        "time": "O(n^2)",
        "space": "O(n^2)",
        "method": "distinctEchoSubstrings",
        "params": [("text", "String")],
        "ret": "int",
        "py": """        n = len(text)
        m1, m2 = 1000000007, 1000000009
        b1, b2 = 31, 37
        h1 = [0] * (n + 1)
        h2 = [0] * (n + 1)
        p1 = [1] * (n + 1)
        p2 = [1] * (n + 1)
        for i, ch in enumerate(text):
            v = ord(ch) - 96
            h1[i + 1] = (h1[i] * b1 + v) % m1
            h2[i + 1] = (h2[i] * b2 + v) % m2
            p1[i + 1] = (p1[i] * b1) % m1
            p2[i + 1] = (p2[i] * b2) % m2
        seen = set()
        for half in range(1, n // 2 + 1):
            pw1, pw2 = p1[half], p2[half]
            for i in range(n - 2 * half + 1):
                a1 = (h1[i + half] - h1[i] * pw1) % m1
                b1v = (h1[i + 2 * half] - h1[i + half] * pw1) % m1
                if a1 == b1v:
                    a2 = (h2[i + half] - h2[i] * pw2) % m2
                    b2v = (h2[i + 2 * half] - h2[i + half] * pw2) % m2
                    if a2 == b2v:
                        seen.add((half, a1, a2))
        return len(seen)""",
        "java": """        int n = text.length();
        long m1 = 1000000007L, m2 = 1000000009L;
        long b1 = 31L, b2 = 37L;
        long[] h1 = new long[n + 1], h2 = new long[n + 1];
        long[] p1 = new long[n + 1], p2 = new long[n + 1];
        p1[0] = p2[0] = 1;
        for (int i = 0; i < n; i++) {
            int v = text.charAt(i) - 'a' + 1;
            h1[i + 1] = (h1[i] * b1 + v) % m1;
            h2[i + 1] = (h2[i] * b2 + v) % m2;
            p1[i + 1] = (p1[i] * b1) % m1;
            p2[i + 1] = (p2[i] * b2) % m2;
        }
        int total = 0;
        for (int half = 1; half <= n / 2; half++) {
            long pw1 = p1[half], pw2 = p2[half];
            HashSet<Long> seen = new HashSet<>();
            for (int i = 0; i + 2 * half <= n; i++) {
                long a1 = (h1[i + half] - h1[i] * pw1 % m1 + m1) % m1;
                long b1v = (h1[i + 2 * half] - h1[i + half] * pw1 % m1 + m1) % m1;
                if (a1 == b1v) {
                    long a2 = (h2[i + half] - h2[i] * pw2 % m2 + m2) % m2;
                    long b2v = (h2[i + 2 * half] - h2[i + half] * pw2 % m2 + m2) % m2;
                    if (a2 == b2v) {
                        seen.add((a1 << 32) ^ a2);
                    }
                }
            }
            total += seen.size();
        }
        return total;""",
        "visible": [
            {"text": "abcabcabc"},
            {"text": "leetcodeleetcode"},
            {"text": "aaaa"},
        ],
        "hidden": [
            {"text": "a"},
            {"text": "aa"},
            {"text": "ab"},
            {"text": "ababab"},
            {"text": "abcdefg"},
            {"text": "aabaaabaa"},
            {"text": "tkfbgwgqvdsbnlblp"},
            {"text": "abacaba" * 20},
            {"text": "a" * 200},
        ],
    },
    {
        "slug": "100-longest-duplicate-substring-length",
        "title": "Longest Duplicate Substring Length",
        "difficulty": "Hard",
        "subtopic": "String Matching",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": "Given a lowercase string `s`, return the length of the longest contiguous substring that occurs at least twice in `s` (the occurrences may overlap). If all characters in `s` are distinct, return `0`.",
        "cons": ["1 <= s.length <= 3 * 10^4", "s consists of lowercase English letters."],
        "hints": [
            "If a duplicated substring of length L exists, then duplicated substrings exist for every length < L—so binary search on L.",
            "For a candidate length L, compute double rolling hashes for every window of length L and check for any hash collision in O(n) time."
        ],
        "explanations": [
            "\"ana\" appears twice in \"banana\" (overlapping at indices 1 and 3), length 3.",
            "All letters in \"abcd\" are distinct, so no duplicate substring exists (length 0).",
            "In \"aaaaa\", \"aaaa\" occurs twice (indices 0..3 and 1..4), length 4."
        ],
        "time": "O(n log n)",
        "space": "O(n)",
        "method": "longestDupSubstringLength",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        n = len(s)
        if n <= 1:
            return 0
        m1, m2 = 1000000007, 1000000009
        b1, b2 = 31, 37
        h1 = [0] * (n + 1)
        h2 = [0] * (n + 1)
        p1 = [1] * (n + 1)
        p2 = [1] * (n + 1)
        for i, ch in enumerate(s):
            v = ord(ch) - 96
            h1[i + 1] = (h1[i] * b1 + v) % m1
            h2[i + 1] = (h2[i] * b2 + v) % m2
            p1[i + 1] = (p1[i] * b1) % m1
            p2[i + 1] = (p2[i] * b2) % m2

        def has_dup(length: int) -> bool:
            seen = set()
            pw1, pw2 = p1[length], p2[length]
            for i in range(n - length + 1):
                x1 = (h1[i + length] - h1[i] * pw1) % m1
                x2 = (h2[i + length] - h2[i] * pw2) % m2
                key = (x1 << 32) ^ x2
                if key in seen:
                    return True
                seen.add(key)
            return False

        lo, hi = 0, n - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if has_dup(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo""",
        "java": """        int n = s.length();
        if (n <= 1) return 0;
        long m1 = 1000000007L, m2 = 1000000009L;
        long b1 = 31L, b2 = 37L;
        long[] h1 = new long[n + 1], h2 = new long[n + 1];
        long[] p1 = new long[n + 1], p2 = new long[n + 1];
        p1[0] = p2[0] = 1;
        for (int i = 0; i < n; i++) {
            int v = s.charAt(i) - 'a' + 1;
            h1[i + 1] = (h1[i] * b1 + v) % m1;
            h2[i + 1] = (h2[i] * b2 + v) % m2;
            p1[i + 1] = (p1[i] * b1) % m1;
            p2[i + 1] = (p2[i] * b2) % m2;
        }
        int lo = 0, hi = n - 1;
        while (lo < hi) {
            int mid = (lo + hi + 1) >>> 1;
            if (hasDup(mid, n, h1, h2, p1[mid], p2[mid], m1, m2)) lo = mid;
            else hi = mid - 1;
        }
        return lo;
    }
    private boolean hasDup(int len, int n, long[] h1, long[] h2, long pw1, long pw2, long m1, long m2) {
        HashSet<Long> seen = new HashSet<>(n - len + 1);
        for (int i = 0; i + len <= n; i++) {
            long x1 = (h1[i + len] - h1[i] * pw1 % m1 + m1) % m1;
            long x2 = (h2[i + len] - h2[i] * pw2 % m2 + m2) % m2;
            long key = (x1 << 32) ^ x2;
            if (!seen.add(key)) return true;
        }
        return false;""",
        "visible": [{"s": "banana"}, {"s": "abcd"}, {"s": "aaaaa"}],
        "hidden": [
            {"s": "a"},
            {"s": "aa"},
            {"s": "ababa"},
            {"s": "mississippi"},
            {"s": "nnpxouomcofdjuujloanjimymadkuepightrfodmauhrsy"},
            {"s": "abcdeabcde"},
            {"s": "abracadabra"},
            {"s": "abcdefghij" * 200},
            {"s": "z" * 1500},
        ],
    },
]


def main():
    existing_slugs = set()
    existing_titles = set()
    for p in (ROOT / "problems").rglob("problem.json"):
        m = re.match(r"^(\d{2,3})-(.+)$", p.parent.name)
        if m:
            existing_slugs.add(m.group(2))
        meta = json.loads(p.read_text(encoding="utf-8"))
        existing_titles.add(meta["title"].lower())

    roster_path = ROOT / "problems" / "roster.json"
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    strings_roster = roster.setdefault("strings", [])
    existing_roster_keys = {row[0] for row in strings_roster}

    for p in TASKS:
        slug_only = p["slug"].split("-", 1)[1]
        folder = BASE / p["slug"]
        if not folder.exists():
            assert slug_only not in existing_slugs, f"Duplicate slug: {slug_only}"
            assert p["title"].lower() not in existing_titles, f"Duplicate title: {p['title']}"
            existing_slugs.add(slug_only)
            existing_titles.add(p["title"].lower())
        folder.mkdir(parents=True, exist_ok=True)

        params = [{"name": n, "type": t} for n, t in p["params"]]
        meta = {
            "title": p["title"],
            "difficulty": p["difficulty"],
            "subtopic": p["subtopic"],
            "companies": p["companies"],
            "description": p["desc"],
            "constraints": p["cons"],
            "hints": p["hints"],
            "examples": [{"explanation": e} for e in p["explanations"]],
            "timeComplexity": p["time"],
            "spaceComplexity": p["space"],
            "compare": p.get("compare", "exact"),
            "signature": {
                "kind": "function",
                "method": p["method"],
                "params": params,
                "returns": p["ret"],
            },
        }
        (folder / "problem.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

        pyparams = "".join(f", {n}: {py_type(t)}" for n, t in p["params"])
        (folder / "solution.py").write_text(
            f"class Solution:\n    def {p['method']}(self{pyparams}) -> {py_type(p['ret'])}:\n"
            + p["py"]
            + "\n",
            encoding="utf-8",
        )

        jparams = ", ".join(f"{t} {n}" for n, t in p["params"])
        (folder / "Solution.java").write_text(
            f"class Solution {{\n    public {p['ret']} {p['method']}({jparams}) {{\n"
            + p["java"]
            + "\n    }\n}\n",
            encoding="utf-8",
        )

        vis_code = repr([{"in": x} for x in p["visible"]])
        hid_code = repr([{"in": x} for x in p["hidden"]])
        (folder / "tests.py").write_text(
            f"def visible():\n    return {vis_code}\n\ndef hidden():\n    return {hid_code}\n",
            encoding="utf-8",
        )

        if p["slug"] not in existing_roster_keys:
            strings_roster.append([p["slug"], p["title"], p["difficulty"], p["subtopic"], None])
            existing_roster_keys.add(p["slug"])

    roster_path.write_text(json.dumps(roster, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(TASKS)} string problems (71-100)")


if __name__ == "__main__":
    main()
