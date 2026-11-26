class Solution {
    public boolean canBeValid(String s, String locked) {
        int n = s.length();
        if (n % 2 == 1) return false;
        Deque<Integer> openLocked = new ArrayDeque<>();
        Deque<Integer> unlocked = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            if (locked.charAt(i) == '0') {
                unlocked.push(i);
            } else if (s.charAt(i) == '(') {
                openLocked.push(i);
            } else {
                if (!openLocked.isEmpty()) {
                    openLocked.pop();
                } else if (!unlocked.isEmpty()) {
                    unlocked.pop();
                } else {
                    return false;
                }
            }
        }
        while (!openLocked.isEmpty() && !unlocked.isEmpty() && openLocked.peek() < unlocked.peek()) {
            openLocked.pop();
            unlocked.pop();
        }
        return openLocked.isEmpty();
    }
}
