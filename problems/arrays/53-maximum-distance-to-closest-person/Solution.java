class Solution {
    public int maxDistToClosest(int[] seats) {
        int last = -1, best = 0;
        for (int i = 0; i < seats.length; i++) if (seats[i] == 1) { best = Math.max(best, last < 0 ? i : (i - last) / 2); last = i; }
        return Math.max(best, seats.length - 1 - last);
    }
}
