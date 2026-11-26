class Solution {
    public int findComplement(int num) {
        long mask = ((long) Integer.highestOneBit(num) << 1) - 1;
        return (int) (num ^ mask);
    }
}
