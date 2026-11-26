class Solution {
    public int[] detectLCGCycle(int a, int c, int m, int seed) {
        long A = a;
        long C = c;
        long M = m;
        long x0 = ((long) seed) % M;
        long tortoise = (A * x0 + C) % M;
        long hare = (A * ((A * x0 + C) % M) + C) % M;
        while (tortoise != hare) {
            tortoise = (A * tortoise + C) % M;
            hare = (A * ((A * hare + C) % M) + C) % M;
        }
        int mu = 0;
        tortoise = x0;
        while (tortoise != hare) {
            tortoise = (A * tortoise + C) % M;
            hare = (A * hare + C) % M;
            mu++;
        }
        int lam = 1;
        hare = (A * tortoise + C) % M;
        while (tortoise != hare) {
            hare = (A * hare + C) % M;
            lam++;
        }
        return new int[]{mu, lam};
    }
}
