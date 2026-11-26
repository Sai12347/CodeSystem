# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation.
# class NestedInteger:
#     def isInteger(self) -> bool:
#         """Returns True if this NestedInteger holds a single integer, rather than a nested list."""
#     def getInteger(self) -> int:
#         """Returns the single integer that this NestedInteger holds, if it holds a single integer."""
#     def getList(self) -> List['NestedInteger']:
#         """Returns the nested list that this NestedInteger holds, if it holds a nested list."""

class NestedIterator:
    def __init__(self, nestedList: List['NestedInteger']):
        # Write your solution here
        pass

    def next(self) -> int:
        return 0

    def hasNext(self) -> bool:
        return False
