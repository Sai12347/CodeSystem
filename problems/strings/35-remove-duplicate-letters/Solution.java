class Solution {
    public String removeDuplicateLetters(String s) {
        int[] last = new int[26]; for (int i = 0; i < s.length(); i++) last[s.charAt(i)-'a'] = i;
        boolean[] used = new boolean[26]; char[] stack = new char[26]; int size = 0;
        for (int i = 0; i < s.length(); i++) { char c = s.charAt(i); int x = c-'a'; if (used[x]) continue; while (size > 0 && stack[size-1] > c && last[stack[size-1]-'a'] > i) used[stack[--size]-'a'] = false; stack[size++] = c; used[x] = true; }
        return new String(stack, 0, size);
    }
}
