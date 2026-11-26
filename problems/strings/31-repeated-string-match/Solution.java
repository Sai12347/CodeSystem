class Solution {
    public int repeatedStringMatch(String a, String b) {
        StringBuilder repeated = new StringBuilder(a); int count = 1;
        while (repeated.length() < b.length()) { repeated.append(a); count++; }
        if (repeated.indexOf(b) >= 0) return count;
        repeated.append(a); return repeated.indexOf(b) >= 0 ? count + 1 : -1;
    }
}
