class Solution {
    public int[] maximizeXor(int[] nums, int[][] queries) {
        int n = nums.length;
        int q = queries.length;
        int[] arr = nums.clone();
        Arrays.sort(arr);
        Integer[] order = new Integer[q];
        for (int i = 0; i < q; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> Integer.compare(queries[a][1], queries[b][1]));

        int maxNodes = n * 31 + 2;
        int[] c0 = new int[maxNodes];
        int[] c1 = new int[maxNodes];
        int nodes = 1;

        int[] ans = new int[q];
        int ptr = 0;
        for (int qi : order) {
            int x = queries[qi][0];
            int m = queries[qi][1];
            while (ptr < n && arr[ptr] <= m) {
                int v = arr[ptr++];
                int node = 0;
                for (int b = 29; b >= 0; b--) {
                    if (((v >> b) & 1) != 0) {
                        if (c1[node] == 0) c1[node] = nodes++;
                        node = c1[node];
                    } else {
                        if (c0[node] == 0) c0[node] = nodes++;
                        node = c0[node];
                    }
                }
            }
            if (ptr == 0) {
                ans[qi] = -1;
            } else {
                int node = 0;
                int best = 0;
                for (int b = 29; b >= 0; b--) {
                    if (((x >> b) & 1) != 0) {
                        if (c0[node] != 0) {
                            best |= 1 << b;
                            node = c0[node];
                        } else {
                            node = c1[node];
                        }
                    } else {
                        if (c1[node] != 0) {
                            best |= 1 << b;
                            node = c1[node];
                        } else {
                            node = c0[node];
                        }
                    }
                }
                ans[qi] = best;
            }
        }
        return ans;
    }
}
