class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        planted=0
        for i,x in enumerate(flowerbed):
            if x==0 and (i==0 or flowerbed[i-1]==0) and (i==len(flowerbed)-1 or flowerbed[i+1]==0):
                planted+=1
                if planted>=n: return True
        return n==0
