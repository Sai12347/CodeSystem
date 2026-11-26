class Solution {
    public String reconstructFromDepths(int[] depths) {
        StringBuilder sb = new StringBuilder(depths.length);
        int openCnt = 0;
        for (int d : depths) {
            if (d == openCnt + 1) {
                openCnt++;
                sb.append('(');
            } else if (openCnt > 0 && d == openCnt) {
                openCnt--;
                sb.append(')');
            } else {
                return "";
            }
        }
        return openCnt == 0 ? sb.toString() : "";
    }
}
