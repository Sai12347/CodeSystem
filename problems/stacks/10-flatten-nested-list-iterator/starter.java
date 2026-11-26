/* This is the interface that allows for creating nested lists.
   You should not implement it, or speculate about its implementation.
   interface NestedInteger {
       public boolean isInteger();
       public Integer getInteger();
       public List<NestedInteger> getList();
   } */

class NestedIterator implements Iterator<Integer> {
    public NestedIterator(List<NestedInteger> nestedList) {
        // Write your solution here
    }

    @Override
    public Integer next() {
        return 0;
    }

    @Override
    public boolean hasNext() {
        return false;
    }
}
