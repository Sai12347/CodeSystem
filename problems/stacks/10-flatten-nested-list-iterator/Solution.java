/* This is the interface that allows for creating nested lists.
   interface NestedInteger {
       public boolean isInteger();
       public Integer getInteger();
       public List<NestedInteger> getList();
   } */

class NestedIterator implements Iterator<Integer> {
    private final Deque<Iterator<NestedInteger>> stack = new ArrayDeque<>();
    private Integer nextVal = null;

    public NestedIterator(List<NestedInteger> nestedList) {
        stack.push(nestedList.iterator());
    }

    @Override
    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        Integer res = nextVal;
        nextVal = null;
        return res;
    }

    @Override
    public boolean hasNext() {
        if (nextVal != null) {
            return true;
        }
        while (!stack.isEmpty()) {
            Iterator<NestedInteger> it = stack.peek();
            if (!it.hasNext()) {
                stack.pop();
                continue;
            }
            NestedInteger item = it.next();
            if (item.isInteger()) {
                nextVal = item.getInteger();
                return true;
            }
            stack.push(item.getList().iterator());
        }
        return false;
    }
}
