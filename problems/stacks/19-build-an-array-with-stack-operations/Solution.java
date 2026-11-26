class Solution {
    public List<String> buildArray(int[] target, int n) {
        List<String> ops = new ArrayList<>();
        int cur = 1;
        for (int val : target) {
            while (cur < val) {
                ops.add("Push");
                ops.add("Pop");
                cur++;
            }
            ops.add("Push");
            cur++;
        }
        return ops;
    }
}
