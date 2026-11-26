class Solution {
    public int differenceOfSumAndDigitSum(int[] nums) {
        int elementSum = 0, digitSum = 0;
        for (int x : nums) { elementSum += x; int y = x; while (y > 0) { digitSum += y % 10; y /= 10; } }
        return Math.abs(elementSum - digitSum);
    }
}
