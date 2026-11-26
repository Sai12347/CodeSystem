class Solution {
    public String orderlyQueue(String s, int k) {
        if (k == 1) {
            String best = s;
            for (int i = 1; i < s.length(); i++) {
                String cand = s.substring(i) + s.substring(0, i);
                if (cand.compareTo(best) < 0) best = cand;
            }
            return best;
        }
        char[] arr = s.toCharArray();
        Arrays.sort(arr);
        return new String(arr);
    }
}
