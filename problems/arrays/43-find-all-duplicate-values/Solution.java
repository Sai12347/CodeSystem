class Solution {
    public int[] findDuplicates(int[] nums) {
        int[] counts = new int[nums.length + 1];
        for (int x : nums) counts[x]++;
        int size = 0; for (int x = 1; x < counts.length; x++) if (counts[x] == 2) size++;
        int[] answer = new int[size]; int at = 0;
        for (int x = 1; x < counts.length; x++) if (counts[x] == 2) answer[at++] = x;
        return answer;
    }
}
