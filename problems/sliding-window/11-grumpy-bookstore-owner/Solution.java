class Solution {
    public int maxSatisfied(int[] customers, int[] grumpy, int minutes) {
        int n = customers.length;
        int base = 0;
        int extra = 0;
        for (int i = 0; i < minutes; i++) {
            if (grumpy[i] == 0) {
                base += customers[i];
            } else {
                extra += customers[i];
            }
        }

        int bestExtra = extra;
        for (int i = minutes; i < n; i++) {
            if (grumpy[i] == 0) {
                base += customers[i];
            } else {
                extra += customers[i];
            }
            if (grumpy[i - minutes] == 1) {
                extra -= customers[i - minutes];
            }
            if (extra > bestExtra) {
                bestExtra = extra;
            }
        }

        return base + bestExtra;
    }
}
