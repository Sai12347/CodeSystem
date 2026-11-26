class Solution {
    public boolean canPartitionKSubsets(int[] nums, int k) {
        int total = 0;
        for (int x : nums) total += x;
        if (total % k != 0) return false;
        int target = total / k;

        Arrays.sort(nums);
        int n = nums.length;
        for (int l = 0, r = n - 1; l < r; l++, r--) {
            int tmp = nums[l];
            nums[l] = nums[r];
            nums[r] = tmp;
        }
        if (nums[0] > target) return false;
        if (k == 1) return true;

        boolean[] failed = new boolean[1 << n];
        return dfs(0, 0, nums, target, (1 << n) - 1, failed);
    }

    private boolean dfs(int mask, int curSum, int[] nums, int target, int full, boolean[] failed) {
        if (mask == full) return true;
        if (failed[mask]) return false;

        int n = nums.length;
        if (curSum == 0) {
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) == 0) {
                    int nxt = nums[i];
                    if (dfs(mask | (1 << i), nxt == target ? 0 : nxt, nums, target, full, failed)) {
                        return true;
                    }
                    break;
                }
            }
        } else {
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) continue;
                if (i > 0 && nums[i] == nums[i - 1] && (mask & (1 << (i - 1))) == 0) continue;
                int nxt = curSum + nums[i];
                if (nxt > target) continue;
                if (dfs(mask | (1 << i), nxt == target ? 0 : nxt, nums, target, full, failed)) {
                    return true;
                }
            }
        }

        failed[mask] = true;
        return false;
    }
}
