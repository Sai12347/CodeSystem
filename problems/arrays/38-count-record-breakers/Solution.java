class Solution {
    public int countRecordBreakers(int[] nums) {
        int count = 0, high = 0; boolean seen = false;
        for (int x : nums) if (!seen || x > high) { count++; high = x; seen = true; }
        return count;
    }
}
