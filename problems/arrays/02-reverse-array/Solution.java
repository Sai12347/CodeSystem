class Solution {
    public void reverseArray(int[] nums) {
        int left = 0, right = nums.length - 1;
        while (left < right) {
            int tmp = nums[left];
            nums[left] = nums[right];
            nums[right] = tmp;
            left++;
            right--;
        }
    }
}
