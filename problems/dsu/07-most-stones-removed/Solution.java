class Solution {
    private static final int OFFSET = 10001;
    private Map<Integer, Integer> parent;
    private Map<Integer, Integer> rank;

    private int find(int x) {
        if (!parent.containsKey(x)) {
            parent.put(x, x);
            rank.put(x, 0);
            return x;
        }
        int cur = x;
        while (parent.get(cur) != cur) {
            int gp = parent.get(parent.get(cur));
            parent.put(cur, gp);
            cur = gp;
        }
        return cur;
    }

    private void union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return;
        int rka = rank.get(ra), rkb = rank.get(rb);
        if (rka < rkb) {
            int tmp = ra;
            ra = rb;
            rb = tmp;
            int tr = rka;
            rka = rkb;
            rkb = tr;
        }
        parent.put(rb, ra);
        if (rka == rkb) rank.put(ra, rka + 1);
    }

    public int removeStones(int[][] stones) {
        parent = new HashMap<>();
        rank = new HashMap<>();

        for (int[] s : stones) {
            union(s[0], s[1] + OFFSET);
        }

        Set<Integer> roots = new HashSet<>();
        for (int node : parent.keySet()) {
            roots.add(find(node));
        }
        return stones.length - roots.size();
    }
}
