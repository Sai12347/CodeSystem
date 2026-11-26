class Solution {
    public boolean validWordAbbreviation(String word, String abbr) {
        int i = 0, j = 0;
        while (j < abbr.length()) {
            char c = abbr.charAt(j);
            if (Character.isDigit(c)) {
                if (c == '0') return false; long skip = 0;
                while (j < abbr.length() && Character.isDigit(abbr.charAt(j))) { skip = skip * 10 + abbr.charAt(j++) - '0'; if (skip > word.length()) return false; }
                i += (int) skip; if (i > word.length()) return false;
            } else { if (i >= word.length() || word.charAt(i) != c) return false; i++; j++; }
        }
        return i == word.length();
    }
}
