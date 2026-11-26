class Solution {
    public int[] findOriginalArray(int[] changed) {
        if ((changed.length & 1) == 1) return new int[0];
        int[] a = changed.clone(); Arrays.sort(a); Map<Integer, Integer> count = new HashMap<>(); for (int x : a) count.put(x, count.getOrDefault(x,0)+1);
        int[] out = new int[changed.length/2]; int at = 0;
        for (int x : a) { int c = count.getOrDefault(x,0); if (c == 0) continue; if (x == 0) { if (c < 2) return new int[0]; count.put(0,c-2); out[at++]=0; } else { int d = count.getOrDefault(2*x,0); if (d == 0) return new int[0]; count.put(x,c-1); count.put(2*x,d-1); out[at++]=x; } }
        return at == out.length ? out : new int[0];
    }
}
