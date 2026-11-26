class Solution {
    public int countBalancedRotations(String s) {
        int bal = 0;
        int minBal = 0;
        int minCnt = 0;
        for (int i = 0; i < s.length(); i++) {
            if (bal < minBal) {
                minBal = bal;
                minCnt = 1;
            } else if (bal == minBal) {
                minCnt++;
            }
            bal += (s.charAt(i) == '(') ? 1 : -1;
        }
        return bal == 0 ? minCnt : 0;
    }
}
