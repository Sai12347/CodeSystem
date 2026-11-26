class Solution:
    def unboundedKnapsack(self, weights: List[int], values: List[int], capacity: int) -> int:
        d=[0]*(capacity+1)
        for w,v in zip(weights,values):
            for c in range(w,capacity+1):d[c]=max(d[c],d[c-w]+v)
        return d[capacity]
