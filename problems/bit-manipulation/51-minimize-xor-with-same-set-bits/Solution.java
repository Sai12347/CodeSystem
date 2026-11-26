class Solution {
    public int minimizeXor(int num1, int num2) {
        int need = Integer.bitCount(num2);
        int res = 0;
        for (int b = 30; b >= 0 && need > 0; b--) {
            if (((num1 >> b) & 1) != 0) {
                res |= 1 << b;
                need--;
            }
        }
        for (int b = 0; b <= 30 && need > 0; b++) {
            if (((res >> b) & 1) == 0) {
                res |= 1 << b;
                need--;
            }
        }
        return res;
    }
}
