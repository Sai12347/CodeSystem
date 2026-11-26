class Solution {
    public int numberOfGoodPairs(int[] nums) {
        Map<Integer, Integer> counts = new HashMap<>(); int answer = 0;
        for (int x : nums) { int seen = counts.getOrDefault(x,0); answer += seen; counts.put(x, seen+1); }
        return answer;
    }
}
