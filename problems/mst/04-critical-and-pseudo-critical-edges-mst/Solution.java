class Solution {
    private static final int INF = Integer.MAX_VALUE;

    private int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    private boolean union(int[] parent, int[] size, int a, int b) {
        int ra = find(parent, a);
        int rb = find(parent, b);
        if (ra == rb) {
            return false;
        }
        if (size[ra] < size[rb]) {
            int tmp = ra;
            ra = rb;
            rb = tmp;
        }
        parent[rb] = ra;
        size[ra] += size[rb];
        return true;
    }

    private int kruskal(int n, int[][] indexed, int skipIdx, int forcePos) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        int weight = 0;
        int used = 0;
        if (forcePos != -1) {
            union(parent, size, indexed[forcePos][0], indexed[forcePos][1]);
            weight += indexed[forcePos][2];
            used++;
        }
        for (int pos = 0; pos < indexed.length; pos++) {
            if (pos == forcePos || indexed[pos][3] == skipIdx) {
                continue;
            }
            if (union(parent, size, indexed[pos][0], indexed[pos][1])) {
                weight += indexed[pos][2];
                used++;
                if (used == n - 1) {
                    break;
                }
            }
        }
        return used == n - 1 ? weight : INF;
    }

    public List<List<Integer>> findCriticalAndPseudoCriticalEdges(int n, int[][] edges) {
        int m = edges.length;
        int[][] indexed = new int[m][4];
        for (int i = 0; i < m; i++) {
            indexed[i][0] = edges[i][0];
            indexed[i][1] = edges[i][1];
            indexed[i][2] = edges[i][2];
            indexed[i][3] = i;
        }
        Arrays.sort(indexed, (a, b) -> Integer.compare(a[2], b[2]));

        int baseMst = kruskal(n, indexed, -1, -1);
        List<Integer> critical = new ArrayList<>();
        List<Integer> pseudo = new ArrayList<>();

        for (int pos = 0; pos < m; pos++) {
            int idx = indexed[pos][3];
            if (kruskal(n, indexed, idx, -1) > baseMst) {
                critical.add(idx);
            } else if (kruskal(n, indexed, -1, pos) == baseMst) {
                pseudo.add(idx);
            }
        }

        Collections.sort(critical);
        Collections.sort(pseudo);
        List<List<Integer>> result = new ArrayList<>(2);
        result.add(critical);
        result.add(pseudo);
        return result;
    }
}
