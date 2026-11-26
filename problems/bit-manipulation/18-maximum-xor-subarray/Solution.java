class Solution {
    public int maxXorSubarray(int[] nums) {
        int maxNodes = (nums.length + 2) * 31;
        int[] c0 = new int[maxNodes];
        int[] c1 = new int[maxNodes];
        Arrays.fill(c0, -1);
        Arrays.fill(c1, -1);
        int size = 1;

        // Insert prefix 0
        int node = 0;
        for (int b = 29; b >= 0; b--) {
            if (c0[node] == -1) c0[node] = size++;
            node = c0[node];
        }

        int pref = 0;
        int best = 0;
        for (int x : nums) {
            pref ^= x;
            node = 0;
            int cand = 0;
            for (int b = 29; b >= 0; b--) {
                int bit = (pref >>> b) & 1;
                if (bit == 0) {
                    if (c1[node] != -1) {
                        cand |= 1 << b;
                        node = c1[node];
                    } else {
                        node = c0[node];
                    }
                } else {
                    if (c0[node] != -1) {
                        cand |= 1 << b;
                        node = c0[node];
                    } else {
                        node = c1[node];
                    }
                }
            }
            if (cand > best) best = cand;

            node = 0;
            for (int b = 29; b >= 0; b--) {
                int bit = (pref >>> b) & 1;
                if (bit == 0) {
                    if (c0[node] == -1) c0[node] = size++;
                    node = c0[node];
                } else {
                    if (c1[node] == -1) c1[node] = size++;
                    node = c1[node];
                }
            }
        }
        return best;
    }
}
