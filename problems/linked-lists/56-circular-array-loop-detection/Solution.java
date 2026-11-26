class Solution {
    private int nextIdx(int[] nums, int idx, boolean forward) {
        int n = nums.length;
        if ((nums[idx] > 0) != forward) {
            return -1;
        }
        int nxt = ((idx + nums[idx]) % n + n) % n;
        if (nxt == idx || nums[nxt] == 0 || (nums[nxt] > 0) != forward) {
            return -1;
        }
        return nxt;
    }

    public boolean circularArrayLoop(int[] nums) {
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            if (nums[i] == 0) {
                continue;
            }
            boolean forward = nums[i] > 0;
            int slow = i;
            int fast = i;
            while (true) {
                slow = nextIdx(nums, slow, forward);
                if (slow == -1) {
                    break;
                }
                fast = nextIdx(nums, fast, forward);
                if (fast != -1) {
                    fast = nextIdx(nums, fast, forward);
                }
                if (fast == -1) {
                    break;
                }
                if (slow == fast) {
                    return true;
                }
            }
            int curr = i;
            while (nums[curr] != 0 && (nums[curr] > 0) == forward) {
                int nxt = ((curr + nums[curr]) % n + n) % n;
                nums[curr] = 0;
                curr = nxt;
            }
        }
        return false;
    }
}
