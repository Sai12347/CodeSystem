class Solution {
    public String pushDominoes(String dominoes) {
        char[] arr = dominoes.toCharArray();
        int n = arr.length;
        int prevI = -1;
        char prevC = 'L';
        for (int i = 0; i <= n; i++) {
            char curC = i < n ? arr[i] : 'R';
            if (curC == '.') continue;
            if (prevC == curC) {
                for (int k = prevI + 1; k < i; k++) arr[k] = curC;
            } else if (prevC == 'R' && curC == 'L') {
                int l = prevI + 1, r = i - 1;
                while (l < r) {
                    arr[l++] = 'R';
                    arr[r--] = 'L';
                }
            }
            prevI = i;
            prevC = curC;
        }
        return new String(arr);
    }
}
