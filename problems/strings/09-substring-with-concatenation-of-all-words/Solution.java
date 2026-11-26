class Solution {
    public List<Integer> findSubstring(String s, String[] words) {
        List<Integer> result = new ArrayList<>();
        if (s == null || words == null || words.length == 0) {
            return result;
        }
        int wordLen = words[0].length();
        int numWords = words.length;
        int totalLen = wordLen * numWords;
        int n = s.length();
        if (n < totalLen) {
            return result;
        }

        Map<String, Integer> need = new HashMap<>();
        for (String w : words) {
            need.put(w, need.getOrDefault(w, 0) + 1);
        }

        for (int offset = 0; offset < wordLen; offset++) {
            int left = offset;
            int matched = 0;
            Map<String, Integer> seen = new HashMap<>();
            for (int right = offset; right + wordLen <= n; right += wordLen) {
                String word = s.substring(right, right + wordLen);
                Integer target = need.get(word);
                if (target != null) {
                    int count = seen.getOrDefault(word, 0) + 1;
                    seen.put(word, count);
                    matched++;
                    while (count > target) {
                        String leftWord = s.substring(left, left + wordLen);
                        seen.put(leftWord, seen.get(leftWord) - 1);
                        matched--;
                        left += wordLen;
                        if (leftWord.equals(word)) {
                            count--;
                        }
                    }
                    if (matched == numWords) {
                        result.add(left);
                        String leftWord = s.substring(left, left + wordLen);
                        seen.put(leftWord, seen.get(leftWord) - 1);
                        matched--;
                        left += wordLen;
                    }
                } else {
                    seen.clear();
                    matched = 0;
                    left = right + wordLen;
                }
            }
        }
        return result;
    }
}
