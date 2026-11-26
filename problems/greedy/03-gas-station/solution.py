class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total=cur=start=0
        for i,(g,c) in enumerate(zip(gas,cost)):
            total+=g-c;cur+=g-c
            if cur<0:start=i+1;cur=0
        return start if total>=0 else -1
