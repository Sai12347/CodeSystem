class RangeMinTree {
    private final int n;
    private final int[] tree,lazy;
    public RangeMinTree(int[] nums) { n=nums.length;tree=new int[4*n];lazy=new int[4*n];build(1,0,n-1,nums); }
    private void build(int p,int l,int r,int[] a) { if(l==r){tree[p]=a[l];return;}int m=(l+r)/2;build(p*2,l,m,a);build(p*2+1,m+1,r,a);tree[p]=Math.min(tree[p*2],tree[p*2+1]); }
    private void apply(int p,int x) { tree[p]+=x;lazy[p]+=x; }
    private void push(int p) { if(lazy[p]!=0){apply(p*2,lazy[p]);apply(p*2+1,lazy[p]);lazy[p]=0;} }
    private void add(int p,int l,int r,int ql,int qr,int x) { if(ql<=l&&r<=qr){apply(p,x);return;}push(p);int m=(l+r)/2;if(ql<=m)add(p*2,l,m,ql,qr,x);if(qr>m)add(p*2+1,m+1,r,ql,qr,x);tree[p]=Math.min(tree[p*2],tree[p*2+1]); }
    public void rangeAdd(int left,int right,int delta) { add(1,0,n-1,left,right,delta); }
    private int query(int p,int l,int r,int ql,int qr) { if(ql<=l&&r<=qr)return tree[p];push(p);int m=(l+r)/2,ans=Integer.MAX_VALUE;if(ql<=m)ans=Math.min(ans,query(p*2,l,m,ql,qr));if(qr>m)ans=Math.min(ans,query(p*2+1,m+1,r,ql,qr));return ans; }
    public int minRange(int left,int right) { return query(1,0,n-1,left,right); }
}
