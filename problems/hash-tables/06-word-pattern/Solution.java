class Solution {
    public boolean wordPattern(String pattern, String s) {
        String[] words = s.split(" ");
        if (words.length != pattern.length()) {
            return false;
        }
        Map<Character, String> charToWord = new HashMap<>();
        Map<String, Character> wordToChar = new HashMap<>();
        for (int i = 0; i < pattern.length(); i++) {
            char ch = pattern.charAt(i);
            String w = words[i];
            String mappedW = charToWord.get(ch);
            if (mappedW != null) {
                if (!mappedW.equals(w)) {
                    return false;
                }
            } else {
                if (wordToChar.containsKey(w)) {
                    return false;
                }
                charToWord.put(ch, w);
                wordToChar.put(w, ch);
            }
        }
        return true;
    }
}
