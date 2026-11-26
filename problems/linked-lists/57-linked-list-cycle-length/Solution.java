class Solution {
    public int cycleLength(int[] next, int start) {
        int slow = start;
        int fast = start;
        while (fast != -1 && next[fast] != -1) {
            slow = next[slow];
            fast = next[next[fast]];
            if (slow == fast) {
                int length = 1;
                int curr = next[slow];
                while (curr != slow) {
                    curr = next[curr];
                    length++;
                }
                return length;
            }
        }
        return 0;
    }
}
