class Solution {
    public int postfixPeakDepth(String[] tokens) {
        int h = 0, peak = 0;
        for (String tok : tokens) {
            if (tok.equals("neg") || tok.equals("abs")) {
                if (h < 1) return -1;
            } else if (tok.equals("+") || tok.equals("-") || tok.equals("*") || tok.equals("/")) {
                if (h < 2) return -1;
                h--;
            } else {
                h++;
                if (h > peak) peak = h;
            }
        }
        return h == 1 ? peak : -1;
    }
}
