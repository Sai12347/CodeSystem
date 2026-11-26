class Solution {
    public int compareVersion(String version1, String version2) {
        String[] a = version1.split("\\.", -1), b = version2.split("\\.", -1);
        for (int i = 0; i < Math.max(a.length, b.length); i++) {
            String x = i < a.length ? a[i].replaceFirst("^0+", "") : "";
            String y = i < b.length ? b[i].replaceFirst("^0+", "") : "";
            if (x.length() != y.length()) return x.length() > y.length() ? 1 : -1;
            int cmp = x.compareTo(y); if (cmp != 0) return cmp > 0 ? 1 : -1;
        }
        return 0;
    }
}
