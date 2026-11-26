interface MountainArray {
    int get(int index);
    int length();
}

class MountainArrayImpl implements MountainArray {
    private final int[] arr;
    private int calls = 0;

    MountainArrayImpl(int[] arr) {
        this.arr = arr;
    }

    @Override
    public int get(int index) {
        calls++;
        if (index < 0 || index >= arr.length) {
            throw new IndexOutOfBoundsException("Index " + index + " out of bounds for length " + arr.length);
        }
        return arr[index];
    }

    @Override
    public int length() {
        return arr.length;
    }

    int getCalls() {
        return calls;
    }
}

class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> raw = (List<Object>) inp.get("mountainArr");
        int[] arr = new int[raw.size()];
        for (int i = 0; i < raw.size(); i++) {
            arr[i] = ((Number) raw.get(i)).intValue();
        }
        int target = ((Number) inp.get("target")).intValue();
        MountainArrayImpl ma = new MountainArrayImpl(arr);
        int res = new Solution().findInMountainArray(target, ma);
        if (ma.getCalls() > 100) {
            return "Exceeded maximum of 100 calls to MountainArray.get() (made " + ma.getCalls() + " calls)";
        }
        return res;
    }
}
