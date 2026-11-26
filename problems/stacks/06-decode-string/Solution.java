class Solution {
    public String decodeString(String s) {
        Deque<StringBuilder> strStack = new ArrayDeque<>();
        Deque<Integer> countStack = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        int k = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch >= '0' && ch <= '9') {
                k = k * 10 + (ch - '0');
            } else if (ch == '[') {
                strStack.push(cur);
                countStack.push(k);
                cur = new StringBuilder();
                k = 0;
            } else if (ch == ']') {
                int repeat = countStack.pop();
                StringBuilder prev = strStack.pop();
                for (int r = 0; r < repeat; r++) {
                    prev.append(cur);
                }
                cur = prev;
            } else {
                cur.append(ch);
            }
        }
        return cur.toString();
    }
}
