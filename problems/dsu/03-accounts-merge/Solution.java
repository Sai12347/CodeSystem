class Solution {
    private int[] parent;
    private int[] rank;

    private int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    private void union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return;
        if (rank[ra] < rank[rb]) {
            int tmp = ra;
            ra = rb;
            rb = tmp;
        }
        parent[rb] = ra;
        if (rank[ra] == rank[rb]) rank[ra]++;
    }

    public List<List<String>> accountsMerge(List<List<String>> accounts) {
        int n = accounts.size();
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        Map<String, Integer> emailToAcc = new HashMap<>();
        for (int i = 0; i < n; i++) {
            List<String> acc = accounts.get(i);
            for (int j = 1; j < acc.size(); j++) {
                String email = acc.get(j);
                Integer prev = emailToAcc.putIfAbsent(email, i);
                if (prev != null) {
                    union(i, prev);
                }
            }
        }

        Map<Integer, List<String>> groups = new HashMap<>();
        for (Map.Entry<String, Integer> entry : emailToAcc.entrySet()) {
            int root = find(entry.getValue());
            groups.computeIfAbsent(root, k -> new ArrayList<>()).add(entry.getKey());
        }

        List<List<String>> res = new ArrayList<>(groups.size());
        for (Map.Entry<Integer, List<String>> entry : groups.entrySet()) {
            List<String> emails = entry.getValue();
            Collections.sort(emails);
            List<String> merged = new ArrayList<>(emails.size() + 1);
            merged.add(accounts.get(entry.getKey()).get(0));
            merged.addAll(emails);
            res.add(merged);
        }
        return res;
    }
}
