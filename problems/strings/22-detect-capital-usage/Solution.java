class Solution {
    public boolean detectCapitalUse(String word) {
        boolean allUpper = true, allLower = true;
        for (int i = 0; i < word.length(); i++) { char c = word.charAt(i); if (Character.isLowerCase(c)) allUpper = false; else allLower = false; }
        boolean title = Character.isUpperCase(word.charAt(0));
        for (int i = 1; i < word.length(); i++) if (!Character.isLowerCase(word.charAt(i))) title = false;
        return allUpper || allLower || title;
    }
}
