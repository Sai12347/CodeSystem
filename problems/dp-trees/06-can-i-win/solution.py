class Solution:
    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        if desiredTotal<=0:return True
        if maxChoosableInteger*(maxChoosableInteger+1)//2<desiredTotal:return False
        memo={}
        def win(mask,remain):
            if mask in memo:return memo[mask]
            for x in range(1,maxChoosableInteger+1):
                bit=1<<(x-1)
                if not mask&bit and (x>=remain or not win(mask|bit,remain-x)):memo[mask]=True;return True
            memo[mask]=False;return False
        return win(0,desiredTotal)
