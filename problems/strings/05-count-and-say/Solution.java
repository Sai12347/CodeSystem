class Solution {
    public String countAndSay(int n) {
        String cur = "1";
        for (int step = 1; step < n; step++) {
            StringBuilder next = new StringBuilder();
            int m = cur.length();
            int i = 0;
            while (i < m) {
                int j = i + 1;
                while (j < m && cur.charAt(j) == cur.charAt(i)) {
                    j++;
                }
                next.append(j - i).append(cur.charAt(i));
                i = j;
            }
            cur = next.toString();
        }
        return cur;
    }
}
