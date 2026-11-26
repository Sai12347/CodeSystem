class Solution {
    public int maxBalancedLength(String[] fragments) {
        int basePairs = 0;
        List<int[]> posGroup = new ArrayList<>();
        List<int[]> negGroup = new ArrayList<>();
        for (String f : fragments) {
            int o = 0, c = 0;
            for (int i = 0; i < f.length(); i++) {
                if (f.charAt(i) == '(') {
                    o++;
                } else if (o > 0) {
                    o--;
                    basePairs++;
                } else {
                    c++;
                }
            }
            if (o >= c) posGroup.add(new int[]{c, o});
            else negGroup.add(new int[]{c, o});
        }
        posGroup.sort((a, b) -> Integer.compare(a[0], b[0]));
        negGroup.sort((a, b) -> Integer.compare(b[1], a[1]));
        int avail = 0;
        int crossPairs = 0;
        for (int[] p : posGroup) {
            int m = Math.min(avail, p[0]);
            crossPairs += m;
            avail = avail - m + p[1];
        }
        for (int[] p : negGroup) {
            int m = Math.min(avail, p[0]);
            crossPairs += m;
            avail = avail - m + p[1];
        }
        return 2 * (basePairs + crossPairs);
    }
}
