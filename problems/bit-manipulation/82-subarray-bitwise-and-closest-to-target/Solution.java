class Solution {
    public int closestToTarget(int[] nums, int target) {
        int ans = Math.abs(nums[0] - target);
        int[] cur = new int[32];
        int[] nxt = new int[32];
        int curLen = 0;
        for (int x : nums) {
            int nxtLen = 0;
            nxt[nxtLen++] = x;
            for (int i = 0; i < curLen; i++) {
                int v = cur[i] & x;
                if (v != nxt[nxtLen - 1]) {
                    nxt[nxtLen++] = v;
                }
            }
            for (int i = 0; i < nxtLen; i++) {
                int d = Math.abs(nxt[i] - target);
                if (d < ans) ans = d;
            }
            if (ans == 0) return 0;
            int[] tmp = cur;
            cur = nxt;
            nxt = tmp;
            curLen = nxtLen;
        }
        return ans;
    }
}
