class Solution {
    public List<List<Integer>> fourSum(int[] nums, int target) {
        Arrays.sort(nums);
        int n = nums.length;
        List<List<Integer>> res = new ArrayList<>();
        long t = target;
        for (int i = 0; i < n - 3; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            if ((long) nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3] > t) break;
            if ((long) nums[i] + nums[n - 3] + nums[n - 2] + nums[n - 1] < t) continue;
            for (int j = i + 1; j < n - 2; j++) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue;
                if ((long) nums[i] + nums[j] + nums[j + 1] + nums[j + 2] > t) break;
                if ((long) nums[i] + nums[j] + nums[n - 2] + nums[n - 1] < t) continue;
                int left = j + 1, right = n - 1;
                long need = t - nums[i] - nums[j];
                while (left < right) {
                    long pair = (long) nums[left] + nums[right];
                    if (pair == need) {
                        res.add(Arrays.asList(nums[i], nums[j], nums[left], nums[right]));
                        left++;
                        right--;
                        while (left < right && nums[left] == nums[left - 1]) left++;
                        while (left < right && nums[right] == nums[right + 1]) right--;
                    } else if (pair < need) {
                        left++;
                    } else {
                        right--;
                    }
                }
            }
        }
        return res;
    }
}
