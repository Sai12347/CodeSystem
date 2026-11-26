class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        neg=(dividend<0) != (divisor<0);a=abs(dividend);b=abs(divisor);q=0
        for i in range(31,-1,-1):
            if (a>>i)>=b:a-=b<<i;q|=1<<i
        if neg:q=-q
        return min(2147483647,max(-2147483648,q))
