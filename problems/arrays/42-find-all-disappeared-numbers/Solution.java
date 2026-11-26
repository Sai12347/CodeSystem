class Solution {
    public int[] findDisappearedNumbers(int[] nums) {
        boolean[] present = new boolean[nums.length + 1];
        for (int x : nums) present[x] = true;
        int count = 0; for (int x = 1; x <= nums.length; x++) if (!present[x]) count++;
        int[] answer = new int[count]; int at = 0;
        for (int x = 1; x <= nums.length; x++) if (!present[x]) answer[at++] = x;
        return answer;
    }
}
