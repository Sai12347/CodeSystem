class VersionControl {
    private int badVersion;

    void setBadVersion(int bad) {
        this.badVersion = bad;
    }

    public boolean isBadVersion(int version) {
        return version >= badVersion;
    }
}

class Adapter {
    public static Object run(Map<String, Object> inp) {
        int n = ((Number) inp.get("n")).intValue();
        int bad = ((Number) inp.get("bad")).intValue();
        Solution sol = new Solution();
        sol.setBadVersion(bad);
        return sol.firstBadVersion(n);
    }
}
