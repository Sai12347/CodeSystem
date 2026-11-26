class Solution {
    public int[] findDiagonalOrder(List<List<Integer>> nums) {
        List<List<Integer>> buckets = new ArrayList<>();
        int total = 0;
        for (int r = nums.size() - 1; r >= 0; r--) {
            List<Integer> row = nums.get(r);
            total += row.size();
            for (int c = 0; c < row.size(); c++) {
                int d = r + c;
                while (buckets.size() <= d) {
                    buckets.add(new ArrayList<>());
                }
                buckets.get(d).add(row.get(c));
            }
        }
        int[] res = new int[total];
        int idx = 0;
        for (List<Integer> b : buckets) {
            for (int v : b) {
                res[idx++] = v;
            }
        }
        return res;
    }
}
