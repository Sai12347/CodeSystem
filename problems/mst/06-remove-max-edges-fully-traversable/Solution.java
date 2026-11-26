class Solution {
    static class DSU {
        int[] parent;
        int[] size;
        int components;

        DSU(int n) {
            parent = new int[n + 1];
            size = new int[n + 1];
            components = n;
            for (int i = 1; i <= n; i++) {
                parent[i] = i;
                size[i] = 1;
            }
        }

        int find(int x) {
            while (parent[x] != x) {
                parent[x] = parent[parent[x]];
                x = parent[x];
            }
            return x;
        }

        boolean union(int a, int b) {
            int ra = find(a);
            int rb = find(b);
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
            components--;
            return true;
        }
    }

    public int maxNumEdgesToRemove(int n, int[][] edges) {
        if (n <= 1) {
            return edges.length;
        }
        DSU alice = new DSU(n);
        DSU bob = new DSU(n);
        int kept = 0;

        for (int[] e : edges) {
            if (e[0] == 3) {
                boolean mergedA = alice.union(e[1], e[2]);
                boolean mergedB = bob.union(e[1], e[2]);
                if (mergedA || mergedB) {
                    kept++;
                }
            }
        }

        for (int[] e : edges) {
            if (e[0] == 1) {
                if (alice.union(e[1], e[2])) {
                    kept++;
                }
            } else if (e[0] == 2) {
                if (bob.union(e[1], e[2])) {
                    kept++;
                }
            }
        }

        if (alice.components != 1 || bob.components != 1) {
            return -1;
        }
        return edges.length - kept;
    }
}
