class Solution {
    public long numOfSubarrays(int[] nums) {
        long even = 1, odd = 0, answer = 0; int parity = 0;
        for (int x : nums) { parity ^= (x & 1); answer += parity == 1 ? even : odd; if (parity == 1) odd++; else even++; }
        return answer;
    }
}
