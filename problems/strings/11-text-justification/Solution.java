class Solution {
    public List<String> fullJustify(String[] words, int maxWidth) {
        List<String> res = new ArrayList<>();
        int i = 0;
        int n = words.length;
        while (i < n) {
            int lineLen = words[i].length();
            int j = i + 1;
            while (j < n && lineLen + 1 + words[j].length() <= maxWidth) {
                lineLen += 1 + words[j].length();
                j++;
            }
            int numWords = j - i;
            StringBuilder sb = new StringBuilder(maxWidth);
            if (j == n || numWords == 1) {
                for (int k = i; k < j; k++) {
                    if (k > i) {
                        sb.append(' ');
                    }
                    sb.append(words[k]);
                }
                while (sb.length() < maxWidth) {
                    sb.append(' ');
                }
            } else {
                int wordsChars = 0;
                for (int k = i; k < j; k++) {
                    wordsChars += words[k].length();
                }
                int totalSpaces = maxWidth - wordsChars;
                int gaps = numWords - 1;
                int base = totalSpaces / gaps;
                int extra = totalSpaces % gaps;
                for (int k = i; k < j - 1; k++) {
                    sb.append(words[k]);
                    int spaces = base + (k - i < extra ? 1 : 0);
                    for (int s = 0; s < spaces; s++) {
                        sb.append(' ');
                    }
                }
                sb.append(words[j - 1]);
            }
            res.add(sb.toString());
            i = j;
        }
        return res;
    }
}
