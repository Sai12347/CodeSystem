class Solution:
    def maximumUnits(self, boxTypes: List[List[int]], truckSize: int) -> int:
        units=0
        for count,value in sorted(boxTypes,key=lambda x:-x[1]):
            take=min(count,truckSize); units+=take*value; truckSize-=take
            if truckSize==0: break
        return units
