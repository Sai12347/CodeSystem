#!/usr/bin/env python3
"""Generate string problems 41-70 for AlgoPlay."""
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
        "slug": "41-repeated-substring-pattern",
        "title": "Repeated Substring Pattern",
        "difficulty": "Easy",
        "subtopic": "String Matching",
        "companies": ["Google", "Amazon", "Microsoft"],
        "desc": "Given a non-empty lowercase string `s`, determine whether `s` can be constructed by taking a non-empty proper substring of `s` and concatenating two or more copies of it together. Return `true` if such a repeating pattern exists, otherwise `false`.",
        "cons": ["1 <= s.length <= 10^4", "s consists of lowercase English letters."],
        "hints": [
            "If s is a repetition of a smaller block, what happens when you concatenate s with itself?",
            "Check whether s appears inside (s + s) after trimming the first and last characters."
        ],
        "explanations": [
            "The substring \"ab\" repeated twice forms \"abab\".",
            "No proper substring can be repeated to form \"aba\".",
            "The substring \"abc\" repeated four times forms \"abcabcabcabc\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "repeatedSubstringPattern",
        "params": [("s", "String")],
        "ret": "boolean",
        "py": """        return s in (s + s)[1:-1]""",
        "java": """        String doubled = s + s;
        return doubled.substring(1, doubled.length() - 1).contains(s);""",
        "visible": [{"s": "abab"}, {"s": "aba"}, {"s": "abcabcabcabc"}],
        "hidden": [
            {"s": "a"},
            {"s": "aa"},
            {"s": "ab"},
            {"s": "abaababaab"},
            {"s": "abac"},
            {"s": "zzzzz"},
            {"s": "abcdabcd"},
            {"s": "abcdabce"},
            {"s": "abcde" * 400},
        ],
    },
    {
        "slug": "42-rotate-string-check",
        "title": "Rotate String Check",
        "difficulty": "Easy",
        "subtopic": "String Matching",
        "companies": ["Amazon", "Apple", "Bloomberg"],
        "desc": "Given two lowercase strings `s` and `goal`, return `true` if and only if `s` can become `goal` after some number of left shifts (possibly zero). A single left shift moves the leftmost character of `s` to the rightmost position.",
        "cons": ["1 <= s.length, goal.length <= 1000", "s and goal consist of lowercase English letters."],
        "hints": [
            "Two strings of different lengths can never be rotations of each other.",
            "Every rotation of s appears as a contiguous substring of s + s."
        ],
        "explanations": [
            "Shifting \"abcde\" left twice yields \"cdeab\".",
            "No rotation of \"abcde\" produces \"abced\".",
            "Zero shifts leaves \"aaa\" equal to \"aaa\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "rotateString",
        "params": [("s", "String"), ("goal", "String")],
        "ret": "boolean",
        "py": """        return len(s) == len(goal) and goal in (s + s)""",
        "java": """        return s.length() == goal.length() && (s + s).contains(goal);""",
        "visible": [
            {"s": "abcde", "goal": "cdeab"},
            {"s": "abcde", "goal": "abced"},
            {"s": "aaa", "goal": "aaa"},
        ],
        "hidden": [
            {"s": "a", "goal": "a"},
            {"s": "a", "goal": "b"},
            {"s": "ab", "goal": "ba"},
            {"s": "abc", "goal": "ab"},
            {"s": "aa", "goal": "a"},
            {"s": "bbbacddceeb", "goal": "ceebbbbacdd"},
            {"s": "gcmbf", "goal": "fgcmb"},
            {"s": "abcd" * 100, "goal": "cdab" * 100},
            {"s": "a" * 300 + "b", "goal": "a" * 150 + "b" + "a" * 150},
        ],
    },
    {
        "slug": "43-longest-happy-prefix",
        "title": "Longest Happy Prefix",
        "difficulty": "Hard",
        "subtopic": "String Matching",
        "companies": ["Google", "Meta", "Microsoft"],
        "desc": "A string is called a happy prefix if it is a non-empty proper prefix of `s` that is also a suffix of `s` (excluding `s` itself). Given a lowercase string `s`, return its longest happy prefix, or an empty string `\"\"` if no happy prefix exists.",
        "cons": ["1 <= s.length <= 10^5", "s contains only lowercase English letters."],
        "hints": [
            "The KMP prefix function (LPS array) computes, for every prefix, the length of its longest proper border.",
            "The answer is simply the first lps[n - 1] characters of s."
        ],
        "explanations": [
            "The prefix \"l\" of length 1 is also a suffix of \"level\".",
            "The prefix \"abab\" of length 4 is also a suffix of \"ababab\".",
            "No non-empty proper prefix of \"leetcode\" is also a suffix."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "longestPrefix",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        n = len(s)
        lps = [0] * n
        length = 0
        for i in range(1, n):
            while length > 0 and s[i] != s[length]:
                length = lps[length - 1]
            if s[i] == s[length]:
                length += 1
                lps[i] = length
        return s[:lps[-1]]""",
        "java": """        int n = s.length();
        int[] lps = new int[n];
        int length = 0;
        for (int i = 1; i < n; i++) {
            while (length > 0 && s.charAt(i) != s.charAt(length)) {
                length = lps[length - 1];
            }
            if (s.charAt(i) == s.charAt(length)) {
                lps[i] = ++length;
            }
        }
        return s.substring(0, lps[n - 1]);""",
        "visible": [{"s": "level"}, {"s": "ababab"}, {"s": "leetcode"}],
        "hidden": [
            {"s": "a"},
            {"s": "aa"},
            {"s": "aaaa"},
            {"s": "abacaba"},
            {"s": "abacabadabacaba"},
            {"s": "abcde"},
            {"s": "aacaa"},
            {"s": "ababa" + "c" + "ababa"},
            {"s": "ab" * 1500 + "a"},
        ],
    },
    {
        "slug": "44-shortest-distance-to-a-character",
        "title": "Shortest Distance to a Character",
        "difficulty": "Easy",
        "subtopic": "String Matching",
        "companies": ["Amazon", "Google", "Uber"],
        "desc": "Given a lowercase string `s` and a single-character string `c` that is guaranteed to occur at least once in `s`, return an integer array `answer` of length `s.length` where `answer[i]` is the shortest distance from index `i` to the closest occurrence of `c` in `s`.",
        "cons": [
            "1 <= s.length <= 10^4",
            "c.length == 1",
            "s and c consist of lowercase English letters, and c occurs at least once in s."
        ],
        "hints": [
            "Run one pass from left to right tracking the most recent index of c.",
            "Run a second pass from right to left taking the minimum distance to the nearest c on the right."
        ],
        "explanations": [
            "The letter 'e' sits at indices 3, 5, 6, and 11, giving minimal distances at every index.",
            "The letter 'b' is at index 3, so distances decrease from 3 down to 0.",
            "Every position is already 'a', so all distances are 0."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "shortestToChar",
        "params": [("s", "String"), ("c", "String")],
        "ret": "int[]",
        "py": """        target = c[0]
        n = len(s)
        ans = [n] * n
        prev = -n
        for i in range(n):
            if s[i] == target:
                prev = i
            ans[i] = i - prev
        prev = 2 * n
        for i in range(n - 1, -1, -1):
            if s[i] == target:
                prev = i
            ans[i] = min(ans[i], prev - i)
        return ans""",
        "java": """        char target = c.charAt(0);
        int n = s.length();
        int[] ans = new int[n];
        int prev = -n;
        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == target) prev = i;
            ans[i] = i - prev;
        }
        prev = 2 * n;
        for (int i = n - 1; i >= 0; i--) {
            if (s.charAt(i) == target) prev = i;
            ans[i] = Math.min(ans[i], prev - i);
        }
        return ans;""",
        "visible": [
            {"s": "loveleetcode", "c": "e"},
            {"s": "aaab", "c": "b"},
            {"s": "aaaa", "c": "a"},
        ],
        "hidden": [
            {"s": "a", "c": "a"},
            {"s": "baaa", "c": "b"},
            {"s": "abaa", "c": "b"},
            {"s": "abaab", "c": "b"},
            {"s": "zzzzxzzzz", "c": "x"},
            {"s": "xyxyxyx", "c": "y"},
            {"s": "mississippi", "c": "s"},
            {"s": "abcdefghij", "c": "a"},
            {"s": "a" * 500 + "z" + "a" * 500, "c": "z"},
        ],
    },
    {
        "slug": "45-number-of-segments-in-a-string",
        "title": "Number of Segments in a String",
        "difficulty": "Easy",
        "subtopic": "Parsing",
        "companies": ["Amazon", "Microsoft", "Adobe"],
        "desc": "Given a string `s`, return the number of segments in the string. A segment is defined as a maximal contiguous sequence of non-space characters.",
        "cons": ["0 <= s.length <= 10^4", "s consists of printable ASCII characters including spaces."],
        "hints": [
            "A new segment starts at index i whenever s[i] is not a space and either i == 0 or s[i - 1] is a space.",
            "Be careful with empty strings, strings containing only spaces, and multiple consecutive spaces."
        ],
        "explanations": [
            "The five segments are \"Hello,\", \"my\", \"name\", \"is\", and \"John\".",
            "There is a single segment \"Hello\".",
            "A string with only spaces has 0 segments."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "countSegments",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        count = 0
        for i, ch in enumerate(s):
            if ch != ' ' and (i == 0 or s[i - 1] == ' '):
                count += 1
        return count""",
        "java": """        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) != ' ' && (i == 0 || s.charAt(i - 1) == ' ')) {
                count++;
            }
        }
        return count;""",
        "visible": [
            {"s": "Hello, my name is John"},
            {"s": "Hello"},
            {"s": "    "},
        ],
        "hidden": [
            {"s": ""},
            {"s": " a "},
            {"s": "a   b   c"},
            {"s": "  leading and trailing  "},
            {"s": "one,two,three"},
            {"s": "foo bar  baz   qux"},
            {"s": "   ! @ # $   "},
            {"s": "singleword"},
            {"s": " ".join(["tok"] * 500)},
        ],
    },
    {
        "slug": "46-ransom-note-construction",
        "title": "Ransom Note Construction",
        "difficulty": "Easy",
        "subtopic": "Anagrams",
        "companies": ["Amazon", "Meta", "Apple"],
        "desc": "Given two lowercase strings `ransomNote` and `magazine`, return `true` if `ransomNote` can be constructed by using the letters from `magazine` and `false` otherwise. Each letter in `magazine` can only be used once in `ransomNote`.",
        "cons": ["1 <= ransomNote.length, magazine.length <= 10^5", "ransomNote and magazine consist of lowercase English letters."],
        "hints": [
            "Count the frequency of each of the 26 lowercase letters in magazine.",
            "Decrement counts for each character in ransomNote; if any count drops below zero, return false."
        ],
        "explanations": [
            "'a' does not appear in \"b\".",
            "\"ab\" only contains one 'a', but \"aa\" needs two.",
            "\"aab\" has two 'a's, enough to build \"aa\"."
        ],
        "time": "O(n + m)",
        "space": "O(1)",
        "method": "canConstruct",
        "params": [("ransomNote", "String"), ("magazine", "String")],
        "ret": "boolean",
        "py": """        counts = [0] * 26
        for ch in magazine:
            counts[ord(ch) - 97] += 1
        for ch in ransomNote:
            idx = ord(ch) - 97
            counts[idx] -= 1
            if counts[idx] < 0:
                return False
        return True""",
        "java": """        int[] counts = new int[26];
        for (int i = 0; i < magazine.length(); i++) {
            counts[magazine.charAt(i) - 'a']++;
        }
        for (int i = 0; i < ransomNote.length(); i++) {
            if (--counts[ransomNote.charAt(i) - 'a'] < 0) return false;
        }
        return true;""",
        "visible": [
            {"ransomNote": "a", "magazine": "b"},
            {"ransomNote": "aa", "magazine": "ab"},
            {"ransomNote": "aa", "magazine": "aab"},
        ],
        "hidden": [
            {"ransomNote": "a", "magazine": "a"},
            {"ransomNote": "abc", "magazine": "cba"},
            {"ransomNote": "abcd", "magazine": "abc"},
            {"ransomNote": "zz", "magazine": "zyz"},
            {"ransomNote": "bg", "magazine": "efjbdfbdgfjhhaiigfhbaejahgfbbgbjagbddfgdiaigdadhcfcj"},
            {"ransomNote": "fffbfg", "magazine": "effjfggbffjdgbjjhhdegh"},
            {"ransomNote": "hello", "magazine": "ollheworld"},
            {"ransomNote": "a" * 1000, "magazine": "a" * 999 + "b"},
            {"ransomNote": "abcde" * 200, "magazine": "edcba" * 200 + "xyz"},
        ],
    },
    {
        "slug": "47-find-the-added-letter",
        "title": "Find the Added Letter",
        "difficulty": "Easy",
        "subtopic": "Anagrams",
        "companies": ["Google", "Amazon", "Adobe"],
        "desc": "You are given two lowercase strings `s` and `t`. String `t` is generated by randomly shuffling `s` and then adding one more lowercase letter at any position. Return the single letter that was added to `t` as a 1-character string.",
        "cons": ["0 <= s.length <= 10^4", "t.length == s.length + 1", "s and t consist of lowercase English letters."],
        "hints": [
            "Every character in s cancels out with its copy in t under XOR or character-code sum.",
            "XOR all character codes in s and t; the remaining value is the added letter."
        ],
        "explanations": [
            "'e' is the extra character present in \"abcde\" but not \"abcd\".",
            "Since s is empty, the only character 'y' in t is the added letter.",
            "\"aab\" has one extra 'a' compared to \"ab\"."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "findTheDifference",
        "params": [("s", "String"), ("t", "String")],
        "ret": "String",
        "py": """        x = 0
        for ch in s:
            x ^= ord(ch)
        for ch in t:
            x ^= ord(ch)
        return chr(x)""",
        "java": """        int x = 0;
        for (int i = 0; i < s.length(); i++) x ^= s.charAt(i);
        for (int i = 0; i < t.length(); i++) x ^= t.charAt(i);
        return String.valueOf((char) x);""",
        "visible": [
            {"s": "abcd", "t": "abcde"},
            {"s": "", "t": "y"},
            {"s": "ab", "t": "aab"},
        ],
        "hidden": [
            {"s": "a", "t": "aa"},
            {"s": "ae", "t": "aea"},
            {"s": "zyx", "t": "wxyz"},
            {"s": "programming", "t": "grmoipargmnz"},
            {"s": "aaaaa", "t": "aaaaaa"},
            {"s": "qwerty", "t": "ytrewqp"},
            {"s": "listen", "t": "silents"},
            {"s": "abcde" * 200, "t": "abcde" * 100 + "q" + "abcde" * 100},
            {"s": "z" * 1000, "t": "z" * 500 + "a" + "z" * 500},
        ],
    },
    {
        "slug": "48-minimum-steps-to-make-two-strings-anagram",
        "title": "Minimum Steps to Make Two Strings Anagram",
        "difficulty": "Medium",
        "subtopic": "Anagrams",
        "companies": ["Amazon", "Bloomberg", "Meta"],
        "desc": "You are given two equal-length lowercase strings `s` and `t`. In one step you can choose any character in `t` and replace it with any other lowercase English letter. Return the minimum number of steps required to make `t` an anagram of `s`.",
        "cons": ["1 <= s.length <= 5 * 10^4", "s.length == t.length", "s and t consist of lowercase English letters."],
        "hints": [
            "Compute the frequency difference freq_s[c] - freq_t[c] for each letter.",
            "Every surplus occurrence in s that is missing from t must be filled by replacing an excess letter in t."
        ],
        "explanations": [
            "Replace 'a' in \"aba\" with 'b' so it becomes \"bab\".",
            "Five characters in \"practice\" must be replaced to match \"leetcode\" frequencies.",
            "\"anagram\" and \"mangaar\" are already anagrams, so 0 steps are needed."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "minSteps",
        "params": [("s", "String"), ("t", "String")],
        "ret": "int",
        "py": """        diff = [0] * 26
        for a, b in zip(s, t):
            diff[ord(a) - 97] += 1
            diff[ord(b) - 97] -= 1
        return sum(v for v in diff if v > 0)""",
        "java": """        int[] diff = new int[26];
        for (int i = 0; i < s.length(); i++) {
            diff[s.charAt(i) - 'a']++;
            diff[t.charAt(i) - 'a']--;
        }
        int steps = 0;
        for (int v : diff) if (v > 0) steps += v;
        return steps;""",
        "visible": [
            {"s": "bab", "t": "aba"},
            {"s": "leetcode", "t": "practice"},
            {"s": "anagram", "t": "mangaar"},
        ],
        "hidden": [
            {"s": "a", "t": "a"},
            {"s": "a", "t": "b"},
            {"s": "aaaa", "t": "bbbb"},
            {"s": "friend", "t": "family"},
            {"s": "xxyyzz", "t": "xxyyzz"},
            {"s": "gctcxyuluxjuxnsvmomlwcrfb", "t": "qijrjrhqqjxjtprybrzpyfyqt"},
            {"s": "abacaba", "t": "bababab"},
            {"s": "abcde" * 400, "t": "edcba" * 400},
            {"s": "a" * 1000 + "b" * 1000, "t": "b" * 1500 + "c" * 500},
        ],
    },
    {
        "slug": "49-minimum-steps-to-make-anagram-by-appending",
        "title": "Minimum Steps to Make Two Strings Anagram II",
        "difficulty": "Medium",
        "subtopic": "Anagrams",
        "companies": ["Amazon", "Google", "Oracle"],
        "desc": "You are given two lowercase strings `s` and `t`. In one step, you can append any lowercase letter to either `s` or `t`. Return the minimum number of steps required to make `s` and `t` anagrams of each other.",
        "cons": ["1 <= s.length, t.length <= 10^5", "s and t consist of lowercase English letters."],
        "hints": [
            "Since you can only append characters, each letter's final count must be at least max(count_s[c], count_t[c]).",
            "The total number of appends equals the sum of |count_s[c] - count_t[c]| over all 26 letters."
        ],
        "explanations": [
            "Append \"co\" and \"ts\" appropriately: total frequency mismatch across all letters is 7.",
            "Both strings are already anagrams, so 0 appends are needed.",
            "\"abc\" and \"def\" share no letters, requiring 6 appends total."
        ],
        "time": "O(n + m)",
        "space": "O(1)",
        "method": "minStepsToAnagram",
        "params": [("s", "String"), ("t", "String")],
        "ret": "int",
        "py": """        diff = [0] * 26
        for ch in s:
            diff[ord(ch) - 97] += 1
        for ch in t:
            diff[ord(ch) - 97] -= 1
        return sum(abs(v) for v in diff)""",
        "java": """        int[] diff = new int[26];
        for (int i = 0; i < s.length(); i++) diff[s.charAt(i) - 'a']++;
        for (int i = 0; i < t.length(); i++) diff[t.charAt(i) - 'a']--;
        int steps = 0;
        for (int v : diff) steps += Math.abs(v);
        return steps;""",
        "visible": [
            {"s": "leetcode", "t": "coats"},
            {"s": "night", "t": "thing"},
            {"s": "abc", "t": "def"},
        ],
        "hidden": [
            {"s": "a", "t": "a"},
            {"s": "a", "t": "b"},
            {"s": "aaaa", "t": "a"},
            {"s": "abac", "t": "cab"},
            {"s": "cotxazilut", "t": "nahrrmcchxwrieqqdwdpneitkxgnt"},
            {"s": "zzzz", "t": "yyyyyy"},
            {"s": "hello", "magazine_no": None} if False else {"s": "hello", "t": "billion"},
            {"s": "a" * 1000, "t": "a" * 400 + "b" * 300},
            {"s": "xyz" * 300, "t": "zyx" * 300},
        ],
    },
    {
        "slug": "50-determine-if-two-strings-are-close",
        "title": "Determine if Two Strings Are Close",
        "difficulty": "Medium",
        "subtopic": "Anagrams",
        "companies": ["Google", "Meta", "Amazon"],
        "desc": "Two lowercase strings are considered close if you can transform one into the other using any number of two operations: (1) swap any two existing characters, or (2) transform every occurrence of one existing character into another existing character and vice versa. Return `true` if `word1` and `word2` are close, and `false` otherwise.",
        "cons": ["1 <= word1.length, word2.length <= 10^5", "word1 and word2 contain only lowercase English letters."],
        "hints": [
            "Operation 1 lets you freely reorder characters, while Operation 2 lets you permute frequency counts among existing distinct characters.",
            "Two strings are close iff they have the same length, the exact same set of distinct characters, and the same sorted list of character frequencies."
        ],
        "explanations": [
            "\"abc\" can become \"bca\" using only character swaps.",
            "Different lengths mean \"a\" and \"aa\" can never be transformed into each other.",
            "Both use {a, b, c} with sorted frequencies [1, 2, 3]."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "closeStrings",
        "params": [("word1", "String"), ("word2", "String")],
        "ret": "boolean",
        "py": """        if len(word1) != len(word2):
            return False
        c1 = [0] * 26
        c2 = [0] * 26
        for ch in word1:
            c1[ord(ch) - 97] += 1
        for ch in word2:
            c2[ord(ch) - 97] += 1
        for i in range(26):
            if (c1[i] == 0) != (c2[i] == 0):
                return False
        c1.sort()
        c2.sort()
        return c1 == c2""",
        "java": """        if (word1.length() != word2.length()) return false;
        int[] c1 = new int[26], c2 = new int[26];
        for (int i = 0; i < word1.length(); i++) {
            c1[word1.charAt(i) - 'a']++;
            c2[word2.charAt(i) - 'a']++;
        }
        for (int i = 0; i < 26; i++) {
            if ((c1[i] == 0) != (c2[i] == 0)) return false;
        }
        Arrays.sort(c1);
        Arrays.sort(c2);
        return Arrays.equals(c1, c2);""",
        "visible": [
            {"word1": "abc", "word2": "bca"},
            {"word1": "a", "word2": "aa"},
            {"word1": "cabbba", "word2": "abbccc"},
        ],
        "hidden": [
            {"word1": "cabbba", "word2": "aabbss"},
            {"word1": "uau", "word2": "ssx"},
            {"word1": "abbzzca", "word2": "babzzcz"},
            {"word1": "a", "word2": "a"},
            {"word1": "a", "word2": "b"},
            {"word1": "aaabbbbccddeeeeefffff", "word2": "aaaaabbcccdddeeeeffff"},
            {"word1": "ab", "word2": "ba"},
            {"word1": "a" * 500 + "b" * 300 + "c" * 200, "word2": "c" * 500 + "a" * 300 + "b" * 200},
            {"word1": "a" * 500 + "b" * 300 + "c" * 200, "word2": "c" * 500 + "a" * 300 + "d" * 200},
        ],
    },
    {
        "slug": "51-longest-palindromic-subsequence",
        "title": "Longest Palindromic Subsequence",
        "difficulty": "Medium",
        "subtopic": "Palindromes",
        "companies": ["Amazon", "Google", "LinkedIn"],
        "desc": "Given a string `s`, return the length of the longest palindromic subsequence in `s`. A subsequence is formed by deleting zero or more characters from `s` without changing the relative order of the remaining characters.",
        "cons": ["1 <= s.length <= 1000", "s consists only of lowercase English letters."],
        "hints": [
            "Let dp[i][j] be the longest palindromic subsequence inside s[i..j].",
            "If s[i] == s[j], dp[i][j] = dp[i + 1][j - 1] + 2; otherwise take max(dp[i + 1][j], dp[i][j - 1]). You can optimize space to O(n)."
        ],
        "explanations": [
            "\"bbbb\" is a palindromic subsequence of length 4.",
            "\"bb\" is the longest palindromic subsequence of length 2.",
            "All characters are distinct, so any single letter gives length 1."
        ],
        "time": "O(n^2)",
        "space": "O(n)",
        "method": "longestPalindromeSubseq",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        n = len(s)
        dp = [0] * n
        for i in range(n - 1, -1, -1):
            dp[i] = 1
            prev_diag = 0
            for j in range(i + 1, n):
                saved = dp[j]
                if s[i] == s[j]:
                    dp[j] = prev_diag + 2
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                prev_diag = saved
        return dp[n - 1]""",
        "java": """        int n = s.length();
        int[] dp = new int[n];
        for (int i = n - 1; i >= 0; i--) {
            dp[i] = 1;
            int prevDiag = 0;
            for (int j = i + 1; j < n; j++) {
                int saved = dp[j];
                if (s.charAt(i) == s.charAt(j)) {
                    dp[j] = prevDiag + 2;
                } else {
                    dp[j] = Math.max(dp[j], dp[j - 1]);
                }
                prevDiag = saved;
            }
        }
        return dp[n - 1];""",
        "visible": [{"s": "bbbab"}, {"s": "cbbd"}, {"s": "abcdef"}],
        "hidden": [
            {"s": "a"},
            {"s": "aa"},
            {"s": "ab"},
            {"s": "racecar"},
            {"s": "agbdba"},
            {"s": "character"},
            {"s": "abacaba"},
            {"s": "zzazz"},
            {"s": "abcde" * 30 + "edcba" * 30},
        ],
    },
    {
        "slug": "52-minimum-insertions-to-make-palindrome",
        "title": "Minimum Insertion Steps to Make a String Palindrome",
        "difficulty": "Hard",
        "subtopic": "Palindromes",
        "companies": ["Google", "Amazon", "Microsoft"],
        "desc": "Given a string `s`, in one step you can insert any character at any index of `s`. Return the minimum number of steps needed to transform `s` into a palindrome.",
        "cons": ["1 <= s.length <= 500", "s consists of lowercase English letters."],
        "hints": [
            "Characters belonging to the longest palindromic subsequence already mirror each other and need no insertions.",
            "The minimum insertions equal len(s) minus the length of the longest palindromic subsequence."
        ],
        "explanations": [
            "\"zzazz\" is already a palindrome, needing 0 insertions.",
            "\"mbadm\" becomes \"mbdadbm\" or \"mdbabdm\" with 2 insertions.",
            "\"leetcode\" needs 5 insertions to become a palindrome."
        ],
        "time": "O(n^2)",
        "space": "O(n)",
        "method": "minInsertions",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        n = len(s)
        dp = [0] * n
        for i in range(n - 1, -1, -1):
            dp[i] = 1
            prev_diag = 0
            for j in range(i + 1, n):
                saved = dp[j]
                if s[i] == s[j]:
                    dp[j] = prev_diag + 2
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                prev_diag = saved
        return n - dp[n - 1]""",
        "java": """        int n = s.length();
        int[] dp = new int[n];
        for (int i = n - 1; i >= 0; i--) {
            dp[i] = 1;
            int prevDiag = 0;
            for (int j = i + 1; j < n; j++) {
                int saved = dp[j];
                if (s.charAt(i) == s.charAt(j)) {
                    dp[j] = prevDiag + 2;
                } else {
                    dp[j] = Math.max(dp[j], dp[j - 1]);
                }
                prevDiag = saved;
            }
        }
        return n - dp[n - 1];""",
        "visible": [{"s": "zzazz"}, {"s": "mbadm"}, {"s": "leetcode"}],
        "hidden": [
            {"s": "a"},
            {"s": "ab"},
            {"s": "aa"},
            {"s": "abcde"},
            {"s": "g"},
            {"s": "no"},
            {"s": "abacaba"},
            {"s": "zjveiiwvc"},
            {"s": "abcdefghij" * 20},
        ],
    },
    {
        "slug": "53-break-a-palindrome",
        "title": "Break a Palindrome",
        "difficulty": "Medium",
        "subtopic": "Palindromes",
        "companies": ["Amazon", "Goldman Sachs", "Uber"],
        "desc": "Given a palindromic string `palindrome` of lowercase English letters, replace exactly one character with any lowercase English letter so that the resulting string is not a palindrome and is the lexicographically smallest one possible. Return the resulting string, or an empty string `\"\"` if it is impossible.",
        "cons": ["1 <= palindrome.length <= 1000", "palindrome consists of lowercase English letters and is a palindrome."],
        "hints": [
            "A single-character string is always a palindrome regardless of what you replace it with.",
            "Scan only the first half (indices 0 to n//2 - 1): change the first non-'a' character to 'a'. If all first-half characters are 'a', change the last character to 'b'."
        ],
        "explanations": [
            "Replacing the first 'b' with 'a' gives \"aaccba\", which is lexicographically smallest and not a palindrome.",
            "Any 1-character string remains a palindrome, so return \"\".",
            "Changing the last 'a' to 'b' gives \"ab\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "breakPalindrome",
        "params": [("palindrome", "String")],
        "ret": "String",
        "py": """        n = len(palindrome)
        if n == 1:
            return ""
        chars = list(palindrome)
        for i in range(n // 2):
            if chars[i] != 'a':
                chars[i] = 'a'
                return "".join(chars)
        chars[-1] = 'b'
        return "".join(chars)""",
        "java": """        int n = palindrome.length();
        if (n == 1) return "";
        char[] chars = palindrome.toCharArray();
        for (int i = 0; i < n / 2; i++) {
            if (chars[i] != 'a') {
                chars[i] = 'a';
                return new String(chars);
            }
        }
        chars[n - 1] = 'b';
        return new String(chars);""",
        "visible": [{"palindrome": "abccba"}, {"palindrome": "a"}, {"palindrome": "aa"}],
        "hidden": [
            {"palindrome": "aba"},
            {"palindrome": "aaa"},
            {"palindrome": "zzz"},
            {"palindrome": "aabaa"},
            {"palindrome": "racecar"},
            {"palindrome": "bb"},
            {"palindrome": "abcdcba"},
            {"palindrome": "a" * 500 + "z" + "a" * 500},
            {"palindrome": "z" * 1000},
        ],
    },
    {
        "slug": "54-construct-k-palindrome-strings",
        "title": "Construct K Palindrome Strings",
        "difficulty": "Medium",
        "subtopic": "Palindromes",
        "companies": ["Amazon", "Microsoft", "Bloomberg"],
        "desc": "Given a lowercase string `s` and an integer `k`, return `true` if you can use every character in `s` to construct exactly `k` non-empty palindrome strings, and `false` otherwise.",
        "cons": ["1 <= s.length <= 10^5", "1 <= k <= 10^5", "s consists of lowercase English letters."],
        "hints": [
            "You cannot form more non-empty strings than there are characters in s.",
            "Each character with an odd frequency must serve as the center of a distinct palindrome, so oddCount <= k is both necessary and sufficient."
        ],
        "explanations": [
            "We can form \"anna\" and \"elble\" using all characters.",
            "\"leetcode\" has 5 odd-frequency letters, so 3 palindromes cannot absorb them all.",
            "Each single character can be its own palindrome when k == len(s)."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "canConstructPalindromes",
        "params": [("s", "String"), ("k", "int")],
        "ret": "boolean",
        "py": """        if k > len(s):
            return False
        mask = 0
        for ch in s:
            mask ^= 1 << (ord(ch) - 97)
        return mask.bit_count() <= k""",
        "java": """        if (k > s.length()) return false;
        int mask = 0;
        for (int i = 0; i < s.length(); i++) {
            mask ^= 1 << (s.charAt(i) - 'a');
        }
        return Integer.bitCount(mask) <= k;""",
        "visible": [
            {"s": "annabelle", "k": 2},
            {"s": "leetcode", "k": 3},
            {"s": "true", "k": 4},
        ],
        "hidden": [
            {"s": "yzyzyzyzyzyzyzy", "k": 2},
            {"s": "cr", "k": 7},
            {"s": "a", "k": 1},
            {"s": "ab", "k": 1},
            {"s": "aabbcc", "k": 1},
            {"s": "aabbcc", "k": 6},
            {"s": "aabbcc", "k": 7},
            {"s": "abcde" * 200 + "f", "k": 1},
            {"s": "abcdefg" * 101, "k": 6},
        ],
    },
    {
        "slug": "55-unique-length-3-palindromic-subsequences",
        "title": "Unique Length-3 Palindromic Subsequences",
        "difficulty": "Medium",
        "subtopic": "Palindromes",
        "companies": ["Meta", "Google", "Amazon"],
        "desc": "Given a lowercase string `s`, return the number of unique palindromes of length 3 that are subsequences of `s`. Even if the same 3-character palindrome can be formed in multiple index combinations, count it only once.",
        "cons": ["3 <= s.length <= 10^5", "s consists of only lowercase English letters."],
        "hints": [
            "A length-3 palindrome has the form X Y X, where X appears at least twice and Y appears strictly between two occurrences of X.",
            "For each of the 26 letters X, find its first and last occurrence in s and count how many distinct characters appear strictly between them."
        ],
        "explanations": [
            "The unique length-3 palindromic subsequences of \"aabca\" are \"aba\", \"aaa\", and \"aca\".",
            "No character repeats in \"adc\", so there are 0 length-3 palindromes.",
            "The unique palindromes in \"bbcbaba\" are \"bbb\", \"bcb\", \"bab\", and \"aba\"."
        ],
        "time": "O(26 * n)",
        "space": "O(1)",
        "method": "countPalindromicSubsequence",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        first = [-1] * 26
        last = [-1] * 26
        for i, ch in enumerate(s):
            idx = ord(ch) - 97
            if first[idx] == -1:
                first[idx] = i
            last[idx] = i
        ans = 0
        for c in range(26):
            if first[c] != -1 and first[c] + 1 < last[c]:
                seen = 0
                for i in range(first[c] + 1, last[c]):
                    seen |= 1 << (ord(s[i]) - 97)
                ans += seen.bit_count()
        return ans""",
        "java": """        int[] first = new int[26];
        int[] last = new int[26];
        Arrays.fill(first, -1);
        for (int i = 0; i < s.length(); i++) {
            int idx = s.charAt(i) - 'a';
            if (first[idx] == -1) first[idx] = i;
            last[idx] = i;
        }
        int ans = 0;
        for (int c = 0; c < 26; c++) {
            if (first[c] != -1 && first[c] + 1 < last[c]) {
                int seen = 0;
                for (int i = first[c] + 1; i < last[c]; i++) {
                    seen |= 1 << (s.charAt(i) - 'a');
                }
                ans += Integer.bitCount(seen);
            }
        }
        return ans;""",
        "visible": [{"s": "aabca"}, {"s": "adc"}, {"s": "bbcbaba"}],
        "hidden": [
            {"s": "aaa"},
            {"s": "aba"},
            {"s": "abb"},
            {"s": "aaaaaaa"},
            {"s": "abccba"},
            {"s": "tlpjzdmtwderpkpmgoyrcxttiheassztncqvnfjeyxxp"},
            {"s": "abcdefghijklmnopqrstuvwxyz" * 2},
            {"s": "a" + "bcdefghij" * 200 + "a"},
            {"s": "xyz" * 1000},
        ],
    },
    {
        "slug": "56-remove-palindromic-subsequences",
        "title": "Remove Palindromic Subsequences",
        "difficulty": "Easy",
        "subtopic": "Palindromes",
        "companies": ["Amazon", "Google", "Bloomberg"],
        "desc": "You are given a non-empty string `s` consisting only of the letters `'a'` and `'b'`. In a single step you can remove one palindromic subsequence from `s` (not necessarily contiguous). Return the minimum number of steps required to make `s` empty.",
        "cons": ["1 <= s.length <= 10^4", "s[i] is either 'a' or 'b'."],
        "hints": [
            "A subsequence of all 'a's is always a palindrome, and a subsequence of all 'b's is also always a palindrome.",
            "Therefore the answer is 1 if s is already a palindrome, and 2 otherwise."
        ],
        "explanations": [
            "\"ababa\" is already a palindrome, so it can be removed in 1 step.",
            "Remove all 'a's in step 1 and all 'b's in step 2 (2 steps total).",
            "Remove \"aba\" or all 'b's first, then the remaining identical letters in step 2."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "removePalindromeSub",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        return 1 if s == s[::-1] else 2""",
        "java": """        int l = 0, r = s.length() - 1;
        while (l < r) {
            if (s.charAt(l++) != s.charAt(r--)) return 2;
        }
        return 1;""",
        "visible": [{"s": "ababa"}, {"s": "abb"}, {"s": "baabb"}],
        "hidden": [
            {"s": "a"},
            {"s": "b"},
            {"s": "ab"},
            {"s": "aa"},
            {"s": "abba"},
            {"s": "ababb"},
            {"s": "b" * 1000},
            {"s": "a" * 500 + "b" + "a" * 500},
            {"s": "a" * 500 + "b" + "a" * 499},
        ],
    },
    {
        "slug": "57-palindrome-partitioning-min-cuts",
        "title": "Palindrome Partitioning Minimum Cuts",
        "difficulty": "Hard",
        "subtopic": "Palindromes",
        "companies": ["Google", "Meta", "Amazon"],
        "desc": "Given a lowercase string `s`, partition `s` such that every substring in the partition is a palindrome. Return the minimum number of cuts needed to create a valid palindromic partitioning of `s`.",
        "cons": ["1 <= s.length <= 2000", "s consists of lowercase English letters."],
        "hints": [
            "Let dp[i] be the minimum cuts needed for prefix s[0..i - 1], with dp[0] = -1.",
            "Expand around every possible palindrome center (odd and even lengths) and relax dp[r + 1] = min(dp[r + 1], dp[l] + 1)."
        ],
        "explanations": [
            "Partitioning \"aab\" into [\"aa\", \"b\"] requires 1 cut.",
            "\"a\" is already a palindrome, needing 0 cuts.",
            "\"ab\" requires 1 cut into [\"a\", \"b\"]."
        ],
        "time": "O(n^2)",
        "space": "O(n)",
        "method": "minCut",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        n = len(s)
        dp = [i - 1 for i in range(n + 1)]
        for center in range(n):
            l = r = center
            while l >= 0 and r < n and s[l] == s[r]:
                if dp[l] + 1 < dp[r + 1]:
                    dp[r + 1] = dp[l] + 1
                l -= 1
                r += 1
            l, r = center, center + 1
            while l >= 0 and r < n and s[l] == s[r]:
                if dp[l] + 1 < dp[r + 1]:
                    dp[r + 1] = dp[l] + 1
                l -= 1
                r += 1
        return dp[n]""",
        "java": """        int n = s.length();
        int[] dp = new int[n + 1];
        for (int i = 0; i <= n; i++) dp[i] = i - 1;
        for (int center = 0; center < n; center++) {
            for (int l = center, r = center; l >= 0 && r < n && s.charAt(l) == s.charAt(r); l--, r++) {
                dp[r + 1] = Math.min(dp[r + 1], dp[l] + 1);
            }
            for (int l = center, r = center + 1; l >= 0 && r < n && s.charAt(l) == s.charAt(r); l--, r++) {
                dp[r + 1] = Math.min(dp[r + 1], dp[l] + 1);
            }
        }
        return dp[n];""",
        "visible": [{"s": "aab"}, {"s": "a"}, {"s": "ab"}],
        "hidden": [
            {"s": "aa"},
            {"s": "aba"},
            {"s": "abccba"},
            {"s": "abcde"},
            {"s": "aabaa"},
            {"s": "cdd"},
            {"s": "leet"},
            {"s": "abacaba" + "xyzzyx" + "abba"},
            {"s": "a" * 300 + "b" + "c" * 300},
        ],
    },
    {
        "slug": "58-can-make-palindrome-from-substring-queries",
        "title": "Can Make Palindrome From Substring Queries",
        "difficulty": "Medium",
        "subtopic": "Palindromes",
        "companies": ["Google", "Meta", "Uber"],
        "desc": "You are given a lowercase string `s` and an array `queries` where `queries[i] = [left, right, k]`. For each query, consider the substring `s[left..right]` (inclusive): you may rearrange its characters in any order and then replace up to `k` characters with any lowercase letter. Return a boolean array where the `i`-th entry is `true` if the substring can be turned into a palindrome, and `false` otherwise.",
        "cons": [
            "1 <= s.length <= 10^5",
            "1 <= queries.length <= 10^5",
            "0 <= left <= right < s.length",
            "0 <= k <= s.length"
        ],
        "hints": [
            "After rearranging, only the parity (odd vs even count) of each of the 26 letters matters.",
            "Maintain a prefix 26-bit XOR mask; the number of odd-frequency letters in [left, right] is popcount(prefix[right + 1] ^ prefix[left]), and you need oddCount // 2 replacements."
        ],
        "explanations": [
            "Query [3,3,0] is \"d\" (already a palindrome); [1,2,0] is \"bc\" (needs 1 change); [0,3,1] is \"abcd\" (4 odd letters require 2 changes); [0,3,2] allows 2 changes; [0,4,1] is \"abcda\" (3 odd letters require 1 change).",
            "With 0 replacements, \"ly\" cannot form a palindrome, while \"b\" with 1 replacement can.",
            "All letters are identical so every substring is already a palindrome."
        ],
        "time": "O(n + q)",
        "space": "O(n + q)",
        "method": "canMakePaliQueries",
        "params": [("s", "String"), ("queries", "int[][]")],
        "ret": "boolean[]",
        "py": """        n = len(s)
        pref = [0] * (n + 1)
        for i, ch in enumerate(s):
            pref[i + 1] = pref[i] ^ (1 << (ord(ch) - 97))
        return [(pref[r + 1] ^ pref[l]).bit_count() // 2 <= k for l, r, k in queries]""",
        "java": """        int n = s.length();
        int[] pref = new int[n + 1];
        for (int i = 0; i < n; i++) {
            pref[i + 1] = pref[i] ^ (1 << (s.charAt(i) - 'a'));
        }
        boolean[] ans = new boolean[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int l = queries[i][0], r = queries[i][1], k = queries[i][2];
            int odd = Integer.bitCount(pref[r + 1] ^ pref[l]);
            ans[i] = (odd / 2) <= k;
        }
        return ans;""",
        "visible": [
            {"s": "abcda", "queries": [[3, 3, 0], [1, 2, 0], [0, 3, 1], [0, 3, 2], [0, 4, 1]]},
            {"s": "lyb", "queries": [[0, 1, 0], [2, 2, 1]]},
            {"s": "aaaa", "queries": [[0, 3, 0], [1, 2, 0]]},
        ],
        "hidden": [
            {"s": "a", "queries": [[0, 0, 0]]},
            {"s": "ab", "queries": [[0, 1, 0], [0, 1, 1]]},
            {"s": "racecar", "queries": [[0, 6, 0], [0, 5, 0], [0, 5, 1]]},
            {"s": "hunu", "queries": [[1, 1, 1], [2, 3, 0], [3, 3, 1], [0, 3, 2], [1, 3, 3], [2, 3, 1], [3, 3, 1], [0, 3, 0], [1, 1, 1], [2, 3, 0]]},
            {"s": "abcdef", "queries": [[0, 5, 2], [0, 5, 3], [0, 4, 2], [0, 4, 1]]},
            {"s": "aabbccdd", "queries": [[0, 7, 0], [1, 6, 0], [1, 5, 0], [1, 5, 1]]},
            {"s": "xyzxyzxyz", "queries": [[0, 8, 1], [0, 8, 0], [0, 5, 0]]},
            {"s": "abcde" * 200, "queries": [[0, 999, 0], [0, 994, 1], [0, 994, 2], [10, 500, 2]]},
            {"s": "abcdefghijklmnopqrstuvwxyz" * 20, "queries": [[0, 519, 0], [0, 25, 12], [0, 25, 13]]},
        ],
    },
    {
        "slug": "59-largest-palindromic-number",
        "title": "Largest Palindromic Number",
        "difficulty": "Medium",
        "subtopic": "Palindromes",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs"],
        "desc": "You are given a string `num` consisting of digits `'0'` through `'9'`. Return the largest palindromic integer (as a string) that can be formed using any subset of digits from `num` in any order, using each digit at most as many times as it appears in `num`. The result must not have leading zeros (except for the single digit `\"0\"`).",
        "cons": ["1 <= num.length <= 10^5", "num consists of digits '0' through '9'."],
        "hints": [
            "Greedily place pairs of the largest available digits from '9' down to '0' in the left half, skipping '0' if the left half is still empty.",
            "Place the largest remaining unused digit (if any) in the center; if both left half and center are empty, return \"0\"."
        ],
        "explanations": [
            "Using pairs of '7' and '4' with '9' in the middle gives \"7449447\".",
            "Only one '9' is available and leading zeros are forbidden, so \"9\" is optimal.",
            "When only zeros exist, the largest valid palindromic integer is \"0\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "largestPalindromic",
        "params": [("num", "String")],
        "ret": "String",
        "py": """        cnt = [0] * 10
        for ch in num:
            cnt[ord(ch) - 48] += 1
        left = []
        for d in range(9, -1, -1):
            if d == 0 and not left:
                break
            pairs = cnt[d] // 2
            if pairs:
                left.append(str(d) * pairs)
                cnt[d] -= pairs * 2
        mid = ""
        for d in range(9, -1, -1):
            if cnt[d] > 0:
                mid = str(d)
                break
        if not left and not mid:
            return "0"
        lstr = "".join(left)
        return lstr + mid + lstr[::-1]""",
        "java": """        int[] cnt = new int[10];
        for (int i = 0; i < num.length(); i++) cnt[num.charAt(i) - '0']++;
        StringBuilder left = new StringBuilder();
        for (int d = 9; d >= 0; d--) {
            if (d == 0 && left.length() == 0) break;
            int pairs = cnt[d] / 2;
            for (int k = 0; k < pairs; k++) left.append((char) ('0' + d));
            cnt[d] -= pairs * 2;
        }
        String mid = "";
        for (int d = 9; d >= 0; d--) {
            if (cnt[d] > 0) {
                mid = String.valueOf((char) ('0' + d));
                break;
            }
        }
        if (left.length() == 0 && mid.isEmpty()) return "0";
        String l = left.toString();
        return l + mid + left.reverse().toString();""",
        "visible": [{"num": "444947137"}, {"num": "00009"}, {"num": "0000"}],
        "hidden": [
            {"num": "0"},
            {"num": "5"},
            {"num": "00011000"},
            {"num": "123456789"},
            {"num": "98765432100123456789"},
            {"num": "000000000"},
            {"num": "99999"},
            {"num": "10001"},
            {"num": "0123456789" * 100},
        ],
    },
    {
        "slug": "60-valid-palindrome-with-k-deletions",
        "title": "Valid Palindrome With At Most K Deletions",
        "difficulty": "Hard",
        "subtopic": "Palindromes",
        "companies": ["Meta", "Google", "Amazon"],
        "desc": "Given a lowercase string `s` and an integer `k`, return `true` if `s` can be turned into a palindrome by removing at most `k` characters from `s`, and `false` otherwise.",
        "cons": ["1 <= s.length <= 1000", "0 <= k <= s.length", "s consists of lowercase English letters."],
        "hints": [
            "Deleting at most k characters to leave a palindrome is equivalent to finding a palindromic subsequence of length at least n - k.",
            "Compute the longest palindromic subsequence length in O(n^2) time and O(n) space, and check whether n - lps <= k."
        ],
        "explanations": [
            "Removing 'b' and 'e' leaves \"acdca\", a palindrome using 2 deletions.",
            "Removing the 'b' at index 1 leaves \"abababa\", a palindrome using 1 deletion.",
            "\"abcdef\" requires 5 deletions to become a 1-character palindrome, so k = 2 is false."
        ],
        "time": "O(n^2)",
        "space": "O(n)",
        "method": "isValidPalindromeK",
        "params": [("s", "String"), ("k", "int")],
        "ret": "boolean",
        "py": """        n = len(s)
        dp = [0] * n
        for i in range(n - 1, -1, -1):
            dp[i] = 1
            prev_diag = 0
            for j in range(i + 1, n):
                saved = dp[j]
                if s[i] == s[j]:
                    dp[j] = prev_diag + 2
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                prev_diag = saved
        return n - dp[n - 1] <= k""",
        "java": """        int n = s.length();
        int[] dp = new int[n];
        for (int i = n - 1; i >= 0; i--) {
            dp[i] = 1;
            int prevDiag = 0;
            for (int j = i + 1; j < n; j++) {
                int saved = dp[j];
                if (s.charAt(i) == s.charAt(j)) {
                    dp[j] = prevDiag + 2;
                } else {
                    dp[j] = Math.max(dp[j], dp[j - 1]);
                }
                prevDiag = saved;
            }
        }
        return n - dp[n - 1] <= k;""",
        "visible": [
            {"s": "abcdeca", "k": 2},
            {"s": "abbababa", "k": 1},
            {"s": "abcdef", "k": 2},
        ],
        "hidden": [
            {"s": "a", "k": 0},
            {"s": "ab", "k": 0},
            {"s": "ab", "k": 1},
            {"s": "racecar", "k": 0},
            {"s": "abcdeca", "k": 1},
            {"s": "bacabaaa", "k": 2},
            {"s": "abcdef", "k": 5},
            {"s": "abcdef", "k": 4},
            {"s": "ab" * 100 + "cd" * 10 + "ba" * 100, "k": 20},
        ],
    },
    {
        "slug": "61-run-length-string-compression",
        "title": "Run-Length String Compression",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Amazon", "Microsoft", "Apple"],
        "desc": "Given a non-empty string `s`, compress consecutive runs of identical characters: for each maximal group of repeating characters, write the character followed by the decimal count if the group length is 2 or more, or just the character alone if the group length is 1. Return the compressed string.",
        "cons": ["1 <= s.length <= 10^4", "s consists of printable ASCII characters."],
        "hints": [
            "Use two pointers: advance j while s[j] == s[i] to measure each run's length.",
            "Append s[i], and append str(runLength) only when runLength > 1."
        ],
        "explanations": [
            "Runs are 'a' x2, 'b' x2, and 'c' x3, yielding \"a2b2c3\".",
            "A single character has run length 1, so no count is appended.",
            "One 'a' followed by twelve 'b's produces \"ab12\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "compressString",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        out = []
        n = len(s)
        i = 0
        while i < n:
            j = i + 1
            while j < n and s[j] == s[i]:
                j += 1
            out.append(s[i])
            if j - i > 1:
                out.append(str(j - i))
            i = j
        return "".join(out)""",
        "java": """        StringBuilder out = new StringBuilder();
        int n = s.length(), i = 0;
        while (i < n) {
            int j = i + 1;
            while (j < n && s.charAt(j) == s.charAt(i)) j++;
            out.append(s.charAt(i));
            if (j - i > 1) out.append(j - i);
            i = j;
        }
        return out.toString();""",
        "visible": [{"s": "aabbccc"}, {"s": "a"}, {"s": "abbbbbbbbbbbb"}],
        "hidden": [
            {"s": "abcdef"},
            {"s": "aa"},
            {"s": "aaabbaa"},
            {"s": "zzzzzzzzzz"},
            {"s": "a111bbb2"},
            {"s": "AAaaBBb"},
            {"s": "   "},
            {"s": "x" * 100 + "y" + "z" * 1000},
            {"s": "ab" * 500},
        ],
    },
    {
        "slug": "62-reverse-words-in-a-string",
        "title": "Reverse Words in a String",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Microsoft", "Amazon", "Apple"],
        "desc": "Given an input string `s` containing words separated by one or more spaces (possibly with leading or trailing spaces), return a string of the words in reverse order separated by a single space with no leading or trailing spaces.",
        "cons": ["1 <= s.length <= 10^4", "s contains English letters, digits, and spaces, and contains at least one word."],
        "hints": [
            "Scan from the right end skipping spaces, extract each word's [start, end] slice, and append it to the result.",
            "Alternatively split on whitespace, reverse the list of non-empty tokens, and join with a single space."
        ],
        "explanations": [
            "Reversing the four words gives \"blue is sky the\".",
            "Leading and trailing spaces are removed when reversing.",
            "Multiple spaces between \"good\" and \"example\" collapse into a single space."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "reverseWords",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        return " ".join(reversed(s.split()))""",
        "java": """        StringBuilder out = new StringBuilder();
        int i = s.length() - 1;
        while (i >= 0) {
            while (i >= 0 && s.charAt(i) == ' ') i--;
            if (i < 0) break;
            int j = i;
            while (i >= 0 && s.charAt(i) != ' ') i--;
            if (out.length() > 0) out.append(' ');
            out.append(s, i + 1, j + 1);
        }
        return out.toString();""",
        "visible": [
            {"s": "the sky is blue"},
            {"s": "  hello world  "},
            {"s": "a good   example"},
        ],
        "hidden": [
            {"s": "word"},
            {"s": "   a   "},
            {"s": "one two"},
            {"s": "  Bob    Loves  Alice   "},
            {"s": "Alice does not even like bob"},
            {"s": "123 456   789"},
            {"s": "a b c d e f"},
            {"s": "   leading"},
            {"s": "   ".join(f"w{i}" for i in range(400))},
        ],
    },
    {
        "slug": "63-license-key-formatting",
        "title": "License Key Formatting",
        "difficulty": "Easy",
        "subtopic": "Parsing",
        "companies": ["Google", "Amazon", "Adobe"],
        "desc": "You are given a license key string `s` consisting of alphanumeric characters and dashes `'-'`, and a positive integer `k`. Reformat the string so that all lowercase letters are converted to uppercase, every group contains exactly `k` characters separated by `'-'`, except the first group which may be shorter than `k` (between 1 and `k` characters). If `s` has no alphanumeric characters, return `\"\"`.",
        "cons": ["1 <= s.length <= 10^5", "1 <= k <= 10^4", "s consists of English letters, digits, and dashes '-'."],
        "hints": [
            "Iterate backward through s ignoring dashes, converting letters to uppercase.",
            "Insert a dash before every k-th appended character (when the current group is full), then reverse at the end."
        ],
        "explanations": [
            "Stripping dashes gives 8 characters, split into two groups of 4: \"5F3Z-2E9W\".",
            "5 characters with k = 2 produce a first group of 1 followed by two groups of 2: \"2-5G-3J\".",
            "No alphanumeric characters exist, so return an empty string."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "licenseKeyFormatting",
        "params": [("s", "String"), ("k", "int")],
        "ret": "String",
        "py": """        clean = s.replace("-", "").upper()
        if not clean:
            return ""
        first = len(clean) % k or k
        parts = [clean[:first]]
        for i in range(first, len(clean), k):
            parts.append(clean[i:i + k])
        return "-".join(parts)""",
        "java": """        StringBuilder sb = new StringBuilder();
        int count = 0;
        for (int i = s.length() - 1; i >= 0; i--) {
            char c = s.charAt(i);
            if (c == '-') continue;
            if (count == k) {
                sb.append('-');
                count = 0;
            }
            sb.append(Character.toUpperCase(c));
            count++;
        }
        return sb.reverse().toString();""",
        "visible": [
            {"s": "5F3Z-2e-9-w", "k": 4},
            {"s": "2-5g-3-J", "k": 2},
            {"s": "---", "k": 3},
        ],
        "hidden": [
            {"s": "a-a-a-a-", "k": 1},
            {"s": "r", "k": 1},
            {"s": "2-4A0r7-4k", "k": 4},
            {"s": "2-4A0r7-4k", "k": 3},
            {"s": "--a-a-a-a--", "k": 2},
            {"s": "abcde", "k": 10},
            {"s": "0123456789", "k": 3},
            {"s": "a-b-c-d-e-f", "k": 2},
            {"s": "ab-cd-" * 500, "k": 7},
        ],
    },
    {
        "slug": "64-excel-column-title-to-number",
        "title": "Excel Sheet Column Number",
        "difficulty": "Easy",
        "subtopic": "Parsing",
        "companies": ["Microsoft", "Amazon", "Apple"],
        "desc": "Given a string `columnTitle` representing a spreadsheet column title (where `'A'` = 1, `'B'` = 2, ..., `'Z'` = 26, `'AA'` = 27, `'AB'` = 28, ...), return its corresponding positive integer column number.",
        "cons": ["1 <= columnTitle.length <= 7", "columnTitle consists only of uppercase English letters.", "columnTitle is in the range [\"A\", \"FXSHRXW\"]."],
        "hints": [
            "This is bijective base-26 positional notation with digits 1..26 instead of 0..25.",
            "Initialize result = 0, and for each character c update result = result * 26 + (ord(c) - ord('A') + 1)."
        ],
        "explanations": [
            "\"A\" maps to 1.",
            "\"AB\" = 1 * 26 + 2 = 28.",
            "\"ZY\" = 26 * 26 + 25 = 701."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "titleToNumber",
        "params": [("columnTitle", "String")],
        "ret": "int",
        "py": """        ans = 0
        for ch in columnTitle:
            ans = ans * 26 + (ord(ch) - 64)
        return ans""",
        "java": """        int ans = 0;
        for (int i = 0; i < columnTitle.length(); i++) {
            ans = ans * 26 + (columnTitle.charAt(i) - 'A' + 1);
        }
        return ans;""",
        "visible": [
            {"columnTitle": "A"},
            {"columnTitle": "AB"},
            {"columnTitle": "ZY"},
        ],
        "hidden": [
            {"columnTitle": "Z"},
            {"columnTitle": "AA"},
            {"columnTitle": "AZ"},
            {"columnTitle": "BA"},
            {"columnTitle": "ZZ"},
            {"columnTitle": "AAA"},
            {"columnTitle": "ABC"},
            {"columnTitle": "FXSHRXW"},
            {"columnTitle": "ZZZZZZ"},
        ],
    },
    {
        "slug": "65-excel-number-to-column-title",
        "title": "Excel Sheet Column Title",
        "difficulty": "Easy",
        "subtopic": "Parsing",
        "companies": ["Microsoft", "Amazon", "Meta"],
        "desc": "Given a positive integer `columnNumber`, return its corresponding spreadsheet column title (where 1 -> `\"A\"`, 26 -> `\"Z\"`, 27 -> `\"AA\"`, 701 -> `\"ZY\"`).",
        "cons": ["1 <= columnNumber <= 2^31 - 1"],
        "hints": [
            "Because there is no zero digit in Excel column titles, subtract 1 from columnNumber before taking modulo 26.",
            "Append chr(ord('A') + rem), divide by 26, and reverse the collected characters at the end."
        ],
        "explanations": [
            "1 corresponds to \"A\".",
            "28 = 1 * 26 + 2 corresponds to \"AB\".",
            "701 = 26 * 26 + 25 corresponds to \"ZY\"."
        ],
        "time": "O(log_26 n)",
        "space": "O(log_26 n)",
        "method": "convertToTitle",
        "params": [("columnNumber", "int")],
        "ret": "String",
        "py": """        out = []
        n = columnNumber
        while n > 0:
            n -= 1
            out.append(chr(65 + n % 26))
            n //= 26
        return "".join(reversed(out))""",
        "java": """        StringBuilder out = new StringBuilder();
        int n = columnNumber;
        while (n > 0) {
            n--;
            out.append((char) ('A' + n % 26));
            n /= 26;
        }
        return out.reverse().toString();""",
        "visible": [
            {"columnNumber": 1},
            {"columnNumber": 28},
            {"columnNumber": 701},
        ],
        "hidden": [
            {"columnNumber": 26},
            {"columnNumber": 27},
            {"columnNumber": 52},
            {"columnNumber": 53},
            {"columnNumber": 702},
            {"columnNumber": 703},
            {"columnNumber": 18278},
            {"columnNumber": 1000000},
            {"columnNumber": 2147483647},
        ],
    },
    {
        "slug": "66-add-binary-strings",
        "title": "Add Binary Strings",
        "difficulty": "Easy",
        "subtopic": "Parsing",
        "companies": ["Meta", "Amazon", "Google"],
        "desc": "Given two non-empty binary strings `a` and `b` consisting of `'0'` and `'1'` (with no leading zeros except for `\"0\"` itself), return their sum as a binary string.",
        "cons": ["1 <= a.length, b.length <= 10^4", "a and b consist only of '0' or '1' characters."],
        "hints": [
            "Add from right to left maintaining a carry bit, just like elementary binary addition.",
            "Continue the loop while either string has remaining digits or carry is non-zero, then reverse the result."
        ],
        "explanations": [
            "11 (3) + 1 (1) = 100 (4) in binary.",
            "1010 (10) + 1011 (11) = 10101 (21) in binary.",
            "0 + 0 = 0."
        ],
        "time": "O(max(|a|, |b|))",
        "space": "O(max(|a|, |b|))",
        "method": "addBinary",
        "params": [("a", "String"), ("b", "String")],
        "ret": "String",
        "py": """        i, j, carry = len(a) - 1, len(b) - 1, 0
        out = []
        while i >= 0 or j >= 0 or carry:
            s = carry
            if i >= 0:
                s += ord(a[i]) - 48
                i -= 1
            if j >= 0:
                s += ord(b[j]) - 48
                j -= 1
            out.append(str(s & 1))
            carry = s >> 1
        return "".join(reversed(out))""",
        "java": """        int i = a.length() - 1, j = b.length() - 1, carry = 0;
        StringBuilder out = new StringBuilder();
        while (i >= 0 || j >= 0 || carry != 0) {
            int sum = carry;
            if (i >= 0) sum += a.charAt(i--) - '0';
            if (j >= 0) sum += b.charAt(j--) - '0';
            out.append(sum & 1);
            carry = sum >> 1;
        }
        return out.reverse().toString();""",
        "visible": [
            {"a": "11", "b": "1"},
            {"a": "1010", "b": "1011"},
            {"a": "0", "b": "0"},
        ],
        "hidden": [
            {"a": "0", "b": "1"},
            {"a": "1", "b": "1"},
            {"a": "1111", "b": "1111"},
            {"a": "100000", "b": "1"},
            {"a": "110110", "b": "101"},
            {"a": "10101010101", "b": "10101010101"},
            {"a": "1" * 64, "b": "1"},
            {"a": "1" * 1000, "b": "1"},
            {"a": "10" * 500, "b": "11" * 500},
        ],
    },
    {
        "slug": "67-validate-ip-address",
        "title": "Validate IP Address",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Meta", "Amazon", "Microsoft"],
        "desc": "Given a string `queryIP`, return `\"IPv4\"` if it is a valid IPv4 address, `\"IPv6\"` if it is a valid IPv6 address, or `\"Neither\"` otherwise. A valid IPv4 address has 4 decimal segments `x1.x2.x3.x4` separated by `'.'`, where each `xi` is in `[0, 255]` with no leading zeros (except `\"0\"`). A valid IPv6 address has 8 hexadecimal segments separated by `':'`, where each segment has length 1 to 4 and consists solely of hex digits `0-9`, `a-f`, or `A-F`.",
        "cons": ["0 <= queryIP.length <= 100", "queryIP consists of English letters, digits, '.', and ':'."],
        "hints": [
            "Check '.' and ':' counts or split preserving empty trailing segments (split(\".\", -1) in Java).",
            "For IPv4 verify 1-3 ASCII digits, value <= 255, and no leading '0' when length > 1; for IPv6 verify length 1..4 and only hex characters."
        ],
        "explanations": [
            "Four decimal octets in [0, 255] without leading zeros form a valid IPv4 address.",
            "Eight groups of 1-4 hex digits form a valid IPv6 address.",
            "256 exceeds the IPv4 octet upper bound of 255."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "validIPAddress",
        "params": [("queryIP", "String")],
        "ret": "String",
        "py": """        if "." in queryIP:
            parts = queryIP.split(".")
            if len(parts) != 4:
                return "Neither"
            for p in parts:
                if not p or len(p) > 3 or not p.isdigit():
                    return "Neither"
                if len(p) > 1 and p[0] == "0":
                    return "Neither"
                if int(p) > 255:
                    return "Neither"
            return "IPv4"
        if ":" in queryIP:
            parts = queryIP.split(":")
            if len(parts) != 8:
                return "Neither"
            hex_chars = set("0123456789abcdefABCDEF")
            for p in parts:
                if not (1 <= len(p) <= 4) or any(ch not in hex_chars for ch in p):
                    return "Neither"
            return "IPv6"
        return "Neither" """,
        "java": """        if (queryIP.indexOf('.') >= 0) {
            String[] parts = queryIP.split("\\\\.", -1);
            if (parts.length != 4) return "Neither";
            for (String p : parts) {
                if (p.isEmpty() || p.length() > 3) return "Neither";
                if (p.length() > 1 && p.charAt(0) == '0') return "Neither";
                int val = 0;
                for (int i = 0; i < p.length(); i++) {
                    char c = p.charAt(i);
                    if (c < '0' || c > '9') return "Neither";
                    val = val * 10 + (c - '0');
                }
                if (val > 255) return "Neither";
            }
            return "IPv4";
        }
        if (queryIP.indexOf(':') >= 0) {
            String[] parts = queryIP.split(":", -1);
            if (parts.length != 8) return "Neither";
            for (String p : parts) {
                if (p.isEmpty() || p.length() > 4) return "Neither";
                for (int i = 0; i < p.length(); i++) {
                    char c = p.charAt(i);
                    boolean ok = (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
                    if (!ok) return "Neither";
                }
            }
            return "IPv6";
        }
        return "Neither";""",
        "visible": [
            {"queryIP": "172.16.254.1"},
            {"queryIP": "2001:0db8:85a3:0:0:8A2E:0370:7334"},
            {"queryIP": "256.256.256.256"},
        ],
        "hidden": [
            {"queryIP": ""},
            {"queryIP": "0.0.0.0"},
            {"queryIP": "01.01.01.01"},
            {"queryIP": "1.1.1.1."},
            {"queryIP": "192.168.1.1a"},
            {"queryIP": "2001:0db8:85a3::8A2E:0370:7334"},
            {"queryIP": "2001:0db8:85a3:0000:0000:8a2e:0370:7334:"},
            {"queryIP": "2001:0db8:85a3:0:0:8A2E:0370:733g"},
            {"queryIP": "ffff:FFFF:0:1:23:456:789a:BcDe"},
        ],
    },
    {
        "slug": "68-fraction-addition-and-subtraction",
        "title": "Fraction Addition and Subtraction",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Goldman Sachs", "Amazon", "Apple"],
        "desc": "Given a string `expression` representing an expression of fraction addition and subtraction (such as `\"-1/2+1/2+1/3\"`), compute the result and return it as an irreducible fraction string `\"numerator/denominator\"` with a positive denominator. If the result is an integer `x`, format it as `\"x/1\"`.",
        "cons": [
            "The input string contains only digits '0'-'9', '/', '+', and '-'.",
            "Each fraction has numerator and denominator in [1, 10], and the expression has between 1 and 10 fractions.",
            "Intermediate and final numerators and denominators fit in a 32-bit signed integer."
        ],
        "hints": [
            "Maintain a running fraction num / den initialized to 0 / 1.",
            "Parse each signed fraction a / b, update num = num * b + a * den and den = den * b, and divide both by gcd(|num|, den) immediately to prevent overflow."
        ],
        "explanations": [
            "-1/2 + 1/2 = 0, formatted as \"0/1\".",
            "-1/2 + 1/2 + 1/3 = 1/3.",
            "1/3 - 1/2 = -1/6."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "fractionAddition",
        "params": [("expression", "String")],
        "ret": "String",
        "py": """        num, den = 0, 1
        i, n = 0, len(expression)
        while i < n:
            sign = 1
            if expression[i] in "+-":
                sign = -1 if expression[i] == "-" else 1
                i += 1
            a = 0
            while i < n and expression[i].isdigit():
                a = a * 10 + (ord(expression[i]) - 48)
                i += 1
            i += 1  # skip '/'
            b = 0
            while i < n and expression[i].isdigit():
                b = b * 10 + (ord(expression[i]) - 48)
                i += 1
            num = num * b + sign * a * den
            den *= b
            g = math.gcd(abs(num), den)
            num //= g
            den //= g
        return f"{num}/{den}" """,
        "java": """        long num = 0, den = 1;
        int i = 0, n = expression.length();
        while (i < n) {
            int sign = 1;
            if (expression.charAt(i) == '+' || expression.charAt(i) == '-') {
                sign = expression.charAt(i++) == '-' ? -1 : 1;
            }
            long a = 0;
            while (i < n && Character.isDigit(expression.charAt(i))) {
                a = a * 10 + (expression.charAt(i++) - '0');
            }
            i++; // skip '/'
            long b = 0;
            while (i < n && Character.isDigit(expression.charAt(i))) {
                b = b * 10 + (expression.charAt(i++) - '0');
            }
            num = num * b + sign * a * den;
            den *= b;
            long g = gcd(Math.abs(num), den);
            num /= g;
            den /= g;
        }
        return num + "/" + den;
    }
    private long gcd(long a, long b) {
        while (b != 0) {
            long t = a % b;
            a = b;
            b = t;
        }
        return a;""",
        "visible": [
            {"expression": "-1/2+1/2"},
            {"expression": "-1/2+1/2+1/3"},
            {"expression": "1/3-1/2"},
        ],
        "hidden": [
            {"expression": "5/3+1/3"},
            {"expression": "1/1"},
            {"expression": "-1/1"},
            {"expression": "7/2+2/3-3/4"},
            {"expression": "-5/2+10/3+7/9"},
            {"expression": "1/2+1/3+1/6"},
            {"expression": "-1/4-1/4-1/4-1/4"},
            {"expression": "1/10+2/10+3/10+4/10"},
            {"expression": "1/2-1/3+1/4-1/5+1/6-1/7+1/8-1/9+1/10"},
        ],
    },
    {
        "slug": "69-complex-number-multiplication",
        "title": "Complex Number Multiplication",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Amazon", "Adobe", "Bloomberg"],
        "desc": "A complex number is represented as a string of the form `\"real+imaginaryi\"` where both `real` and `imaginary` are signed integers in `[-100, 100]` (for example `\"1+-1i\"`). Given two such strings `num1` and `num2`, return their product formatted in the same `\"real+imaginaryi\"` representation.",
        "cons": ["num1 and num2 are valid complex number strings of the form \"a+bi\" with -100 <= a, b <= 100."],
        "hints": [
            "Split each string on '+' and strip the trailing 'i' from the second part to parse integers (a, b) and (c, d).",
            "Since i^2 = -1, the product is (a*c - b*d) + (a*d + b*c)i."
        ],
        "explanations": [
            "(1 + i) * (1 + i) = 1 + 2i + i^2 = 0 + 2i.",
            "(1 - i) * (1 - i) = 1 - 2i + i^2 = 0 + -2i.",
            "(3 + 2i) * (1 + 4i) = (3 - 8) + (12 + 2)i = -5+14i."
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "complexNumberMultiply",
        "params": [("num1", "String"), ("num2", "String")],
        "ret": "String",
        "py": """        p1 = num1.index('+')
        p2 = num2.index('+')
        a, b = int(num1[:p1]), int(num1[p1 + 1:-1])
        c, d = int(num2[:p2]), int(num2[p2 + 1:-1])
        return f"{a * c - b * d}+{a * d + b * c}i" """,
        "java": """        int p1 = num1.indexOf('+'), p2 = num2.indexOf('+');
        int a = Integer.parseInt(num1.substring(0, p1));
        int b = Integer.parseInt(num1.substring(p1 + 1, num1.length() - 1));
        int c = Integer.parseInt(num2.substring(0, p2));
        int d = Integer.parseInt(num2.substring(p2 + 1, num2.length() - 1));
        return (a * c - b * d) + "+" + (a * d + b * c) + "i";""",
        "visible": [
            {"num1": "1+1i", "num2": "1+1i"},
            {"num1": "1+-1i", "num2": "1+-1i"},
            {"num1": "3+2i", "num2": "1+4i"},
        ],
        "hidden": [
            {"num1": "0+0i", "num2": "0+0i"},
            {"num1": "0+1i", "num2": "0+1i"},
            {"num1": "-1+0i", "num2": "5+-3i"},
            {"num1": "78+-76i", "num2": "-86+72i"},
            {"num1": "100+100i", "num2": "100+100i"},
            {"num1": "-100+-100i", "num2": "-100+-100i"},
            {"num1": "20+22i", "num2": "-18+-10i"},
            {"num1": "1+0i", "num2": "0+-1i"},
            {"num1": "-50+25i", "num2": "40+-20i"},
        ],
    },
    {
        "slug": "70-basic-calculator-ii",
        "title": "Basic Calculator II",
        "difficulty": "Medium",
        "subtopic": "Parsing",
        "companies": ["Meta", "Amazon", "Microsoft"],
        "desc": "Given a valid arithmetic expression string `s` containing non-negative integers, the operators `+`, `-`, `*`, `/`, and optional spaces, evaluate and return its integer value. Multiplication and division have higher precedence than addition and subtraction, and integer division truncates toward zero.",
        "cons": [
            "1 <= s.length <= 3 * 10^5",
            "s consists of digits, '+', '-', '*', '/', and spaces.",
            "All intermediate results and the final answer fit in a 32-bit signed integer; division by zero never occurs."
        ],
        "hints": [
            "Process left to right remembering the previous operator and the last evaluated term.",
            "For '+' or '-', add the last term to the running total and start a new term; for '*' or '/', update the last term in place using truncation toward zero."
        ],
        "explanations": [
            "2 * 2 = 4, then 3 + 4 = 7.",
            "3 / 2 truncates toward zero to 1.",
            "5 / 2 = 2, then 3 + 2 = 5."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "calculate",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        total = 0
        last = 0
        num = 0
        op = '+'
        n = len(s)
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + (ord(ch) - 48)
            if (not ch.isdigit() and ch != ' ') or i == n - 1:
                if op == '+':
                    total += last
                    last = num
                elif op == '-':
                    total += last
                    last = -num
                elif op == '*':
                    last *= num
                else:
                    last = int(last / num)
                op = ch
                num = 0
        return total + last""",
        "java": """        int total = 0, last = 0, num = 0;
        char op = '+';
        int n = s.length();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch >= '0' && ch <= '9') {
                num = num * 10 + (ch - '0');
            }
            if ((ch < '0' || ch > '9') && ch != ' ' || i == n - 1) {
                if (op == '+') {
                    total += last;
                    last = num;
                } else if (op == '-') {
                    total += last;
                    last = -num;
                } else if (op == '*') {
                    last *= num;
                } else {
                    last /= num;
                }
                op = ch;
                num = 0;
            }
        }
        return total + last;""",
        "visible": [
            {"s": "3+2*2"},
            {"s": " 3/2 "},
            {"s": " 3+5 / 2 "},
        ],
        "hidden": [
            {"s": "0"},
            {"s": "42"},
            {"s": "14-3/2"},
            {"s": "1-1+1"},
            {"s": "100000000/1/2/3/4/5/6/7/8/9/10"},
            {"s": "2*3*4-5*6/3+7"},
            {"s": "1 + 2 * 3 - 4 / 2 + 5 * 6 - 7 / 3"},
            {"s": "0-2147483647"},
            {"s": "+".join(["10*2-5/2"] * 200)},
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
    print(f"Generated {len(TASKS)} string problems (41-70)")


if __name__ == "__main__":
    main()
