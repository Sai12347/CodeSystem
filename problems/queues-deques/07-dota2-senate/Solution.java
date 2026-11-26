class Solution {
    public String predictPartyVictory(String senate) {
        int n = senate.length();
        Deque<Integer> radiant = new ArrayDeque<>();
        Deque<Integer> dire = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            if (senate.charAt(i) == 'R') {
                radiant.offerLast(i);
            } else {
                dire.offerLast(i);
            }
        }
        while (!radiant.isEmpty() && !dire.isEmpty()) {
            int r = radiant.pollFirst();
            int d = dire.pollFirst();
            if (r < d) {
                radiant.offerLast(r + n);
            } else {
                dire.offerLast(d + n);
            }
        }
        return radiant.isEmpty() ? "Dire" : "Radiant";
    }
}
