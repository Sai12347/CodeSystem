class RangeMinTree:
    def __init__(self, nums: List[int]):
        self.n=len(nums)
        self.tree=[0]*(4*self.n)
        self.lazy=[0]*(4*self.n)
        self._build(1,0,self.n-1,nums)

    def _build(self,p,l,r,a):
        if l==r:
            self.tree[p]=a[l]
            return
        m=(l+r)//2
        self._build(p*2,l,m,a);self._build(p*2+1,m+1,r,a)
        self.tree[p]=min(self.tree[p*2],self.tree[p*2+1])

    def _apply(self,p,value):
        self.tree[p]+=value;self.lazy[p]+=value

    def _push(self,p):
        if self.lazy[p]:
            self._apply(p*2,self.lazy[p]);self._apply(p*2+1,self.lazy[p]);self.lazy[p]=0

    def _add(self,p,l,r,ql,qr,value):
        if ql<=l and r<=qr:
            self._apply(p,value);return
        self._push(p);m=(l+r)//2
        if ql<=m:self._add(p*2,l,m,ql,qr,value)
        if qr>m:self._add(p*2+1,m+1,r,ql,qr,value)
        self.tree[p]=min(self.tree[p*2],self.tree[p*2+1])

    def rangeAdd(self,left: int,right: int,delta: int) -> None:
        self._add(1,0,self.n-1,left,right,delta)

    def _query(self,p,l,r,ql,qr):
        if ql<=l and r<=qr:return self.tree[p]
        self._push(p);m=(l+r)//2;ans=float('inf')
        if ql<=m:ans=min(ans,self._query(p*2,l,m,ql,qr))
        if qr>m:ans=min(ans,self._query(p*2+1,m+1,r,ql,qr))
        return ans

    def minRange(self,left: int,right: int) -> int:
        return self._query(1,0,self.n-1,left,right)
