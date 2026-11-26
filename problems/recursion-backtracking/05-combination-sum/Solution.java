class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> res = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        dfs(candidates, 0, target, path, res);
        return res;
    }

    private void dfs(int[] candidates, int start, int rem, List<Integer> path, List<List<Integer>> res) {
        if (rem == 0) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < candidates.length; i++) {
            if (candidates[i] > rem) {
                break;
            }
            path.add(candidates[i]);
            dfs(candidates, i, rem - candidates[i], path, res);
            path.remove(path.size() - 1);
        }
    }
}
