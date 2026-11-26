class Solution {
    public boolean checkValidString(String s) {
        Deque<Integer> opens = new ArrayDeque<>();
        Deque<Integer> stars = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                opens.push(i);
            } else if (ch == '*') {
                stars.push(i);
            } else {
                if (!opens.isEmpty()) {
                    opens.pop();
                } else if (!stars.isEmpty()) {
                    stars.pop();
                } else {
                    return false;
                }
            }
        }
        while (!opens.isEmpty() && !stars.isEmpty()) {
            if (opens.peek() < stars.peek()) {
                opens.pop();
                stars.pop();
            } else {
                return false;
            }
        }
        return opens.isEmpty();
    }
}
