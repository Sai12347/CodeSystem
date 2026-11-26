class Solution {
    public List<List<Integer>> combinationSum3(int k, int n) {
        List<List<Integer>> res = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        dfs(1, k, n, path, res);
        return res;
    }

    private void dfs(int start, int need, int rem, List<Integer> path, List<List<Integer>> res) {
        if (need == 0) {
            if (rem == 0) {
                res.add(new ArrayList<>(path));
            }
            return;
        }
        int maxStart = 10 - need;
        for (int num = start; num <= maxStart; num++) {
            int minSum = need * (2 * num + need - 1) / 2;
            if (minSum > rem) {
                break;
            }
            int maxSum = num + (need - 1) * (20 - need) / 2;
            if (maxSum < rem) {
                continue;
            }
            path.add(num);
            dfs(num + 1, need - 1, rem - num, path, res);
            path.remove(path.size() - 1);
        }
    }
}
