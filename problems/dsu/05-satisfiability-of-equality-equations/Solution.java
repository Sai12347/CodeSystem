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

    public boolean equationsPossible(String[] equations) {
        parent = new int[26];
        rank = new int[26];
        for (int i = 0; i < 26; i++) parent[i] = i;

        for (String eq : equations) {
            if (eq.charAt(1) == '=') {
                union(eq.charAt(0) - 'a', eq.charAt(3) - 'a');
            }
        }
        for (String eq : equations) {
            if (eq.charAt(1) == '!') {
                if (find(eq.charAt(0) - 'a') == find(eq.charAt(3) - 'a')) {
                    return false;
                }
            }
        }
        return true;
    }
}
