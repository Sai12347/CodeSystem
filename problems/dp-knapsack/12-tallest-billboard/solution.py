class Solution:
    def tallestBillboard(self, rods: List[int]) -> int:
        d={0:0}
        for h in rods:
            nd=dict(d)
            for diff,short in d.items():
                nd[diff+h]=max(nd.get(diff+h,0),short)
                nd[abs(diff-h)]=max(nd.get(abs(diff-h),0),short+min(diff,h))
            d=nd
        return d[0]
