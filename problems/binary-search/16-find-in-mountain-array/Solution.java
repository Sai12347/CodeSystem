/* This is MountainArray's API interface.
   interface MountainArray {
       public int get(int index);
       public int length();
   } */

class Solution {
    public int findInMountainArray(int target, MountainArray mountainArr) {
        int n = mountainArr.length();

        // 1. Find the peak index in [1, n - 2]
        int lo = 1;
        int hi = n - 2;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (mountainArr.get(mid) < mountainArr.get(mid + 1)) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        int peak = lo;

        // 2. Binary search strictly increasing left half [0, peak]
        lo = 0;
        hi = peak;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int val = mountainArr.get(mid);
            if (val == target) {
                return mid;
            }
            if (val < target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }

        // 3. Binary search strictly decreasing right half [peak + 1, n - 1]
        lo = peak + 1;
        hi = n - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int val = mountainArr.get(mid);
            if (val == target) {
                return mid;
            }
            if (val > target) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }

        return -1;
    }
}
