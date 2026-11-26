class Solution {
    public long countKDifference(int[] nums, int k) {
        Map<Integer, Long> counts = new HashMap<>(); for (int x : nums) counts.put(x, counts.getOrDefault(x,0L)+1);
        long answer = 0;
        if (k == 0) { for (long c : counts.values()) answer += c*(c-1)/2; }
        else for (Map.Entry<Integer,Long> e : counts.entrySet()) answer += e.getValue()*counts.getOrDefault(e.getKey()+k,0L);
        return answer;
    }
}
