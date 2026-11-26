class Solution:
    def fallingSquares(self, positions: List[List[int]]) -> List[int]:
        coords=sorted({x for left,size in positions for x in (left,left+size)})
        n=len(coords)-1;tree=[0]*(4*n);lazy=[0]*(4*n);has=[False]*(4*n)
        def push(p):
            if has[p]:
                for c in (p*2,p*2+1):tree[c]=lazy[p];lazy[c]=lazy[p];has[c]=True
                has[p]=False
        def query(p,l,r,a,b):
            if a<=l and r<=b:return tree[p]
            push(p);m=(l+r)//2;ans=0
            if a<=m:ans=max(ans,query(p*2,l,m,a,b))
            if b>m:ans=max(ans,query(p*2+1,m+1,r,a,b))
            return ans
        def assign(p,l,r,a,b,v):
            if a<=l and r<=b:tree[p]=v;lazy[p]=v;has[p]=True;return
            push(p);m=(l+r)//2
            if a<=m:assign(p*2,l,m,a,b,v)
            if b>m:assign(p*2+1,m+1,r,a,b,v)
            tree[p]=max(tree[p*2],tree[p*2+1])
        out=[];overall=0
        for left,size in positions:
            a=bisect.bisect_left(coords,left);b=bisect.bisect_left(coords,left+size)-1
            h=query(1,0,n-1,a,b)+size;assign(1,0,n-1,a,b,h);overall=max(overall,h);out.append(overall)
        return out
