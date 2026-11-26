class Solution {
    public long[] regexLengthBounds(String regex) {
        Deque<long[]> stack = new ArrayDeque<>();
        long hasAlt = 0, altMin = 0, altMax = 0, curMin = 0, curMax = 0;
        boolean hasLast = false;
        long lastMin = 0, lastMax = 0;
        int i = 0, n = regex.length();
        while (i < n) {
            char ch = regex.charAt(i);
            if (ch >= 'a' && ch <= 'z') {
                if (hasLast) {
                    curMin += lastMin;
                    curMax += lastMax;
                }
                hasLast = true;
                lastMin = 1;
                lastMax = 1;
                i++;
            } else if (ch == '(') {
                if (hasLast) {
                    curMin += lastMin;
                    curMax += lastMax;
                    hasLast = false;
                }
                stack.push(new long[]{hasAlt, altMin, altMax, curMin, curMax});
                hasAlt = 0; altMin = 0; altMax = 0; curMin = 0; curMax = 0;
                i++;
            } else if (ch == '|') {
                if (hasLast) {
                    curMin += lastMin;
                    curMax += lastMax;
                    hasLast = false;
                }
                if (hasAlt == 0) {
                    hasAlt = 1;
                    altMin = curMin;
                    altMax = curMax;
                } else {
                    altMin = Math.min(altMin, curMin);
                    altMax = Math.max(altMax, curMax);
                }
                curMin = 0; curMax = 0;
                i++;
            } else if (ch == ')') {
                if (hasLast) {
                    curMin += lastMin;
                    curMax += lastMax;
                    hasLast = false;
                }
                long gMin = (hasAlt == 0) ? curMin : Math.min(altMin, curMin);
                long gMax = (hasAlt == 0) ? curMax : Math.max(altMax, curMax);
                long[] prev = stack.pop();
                hasAlt = prev[0];
                altMin = prev[1];
                altMax = prev[2];
                curMin = prev[3];
                curMax = prev[4];
                hasLast = true;
                lastMin = gMin;
                lastMax = gMax;
                i++;
            } else if (ch == '?') {
                lastMin = 0;
                i++;
            } else if (ch == '{') {
                int j = regex.indexOf('}', i);
                String body = regex.substring(i + 1, j);
                int comma = body.indexOf(',');
                long lo, hi;
                if (comma >= 0) {
                    lo = Long.parseLong(body.substring(0, comma));
                    hi = Long.parseLong(body.substring(comma + 1));
                } else {
                    lo = hi = Long.parseLong(body);
                }
                lastMin *= lo;
                lastMax *= hi;
                i = j + 1;
            } else {
                i++;
            }
        }
        if (hasLast) {
            curMin += lastMin;
            curMax += lastMax;
        }
        if (hasAlt == 0) return new long[]{curMin, curMax};
        return new long[]{Math.min(altMin, curMin), Math.max(altMax, curMax)};
    }
}
