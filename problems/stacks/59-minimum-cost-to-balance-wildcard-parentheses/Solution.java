class Solution {
    public long minCostToBalance(String s, int[] openCost, int[] closeCost) {
        int n = s.length();
        if (n % 2 == 1) return -1L;
        int bal = 0;
        long cost = 0L;
        PriorityQueue<Long> pq = new PriorityQueue<>();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                bal++;
            } else if (ch == ')') {
                bal--;
            } else {
                bal--;
                cost += closeCost[i];
                pq.offer((long) openCost[i] - (long) closeCost[i]);
            }
            while (bal < 0) {
                if (pq.isEmpty()) return -1L;
                cost += pq.poll();
                bal += 2;
            }
        }
        return bal == 0 ? cost : -1L;
    }
}
