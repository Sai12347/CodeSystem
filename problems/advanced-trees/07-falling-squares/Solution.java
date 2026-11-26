class Solution {
    int[] tree,lazy;boolean[] has;
    void push(int p){if(has[p]){for(int c=2*p;c<=2*p+1;c++){tree[c]=lazy[p];lazy[c]=lazy[p];has[c]=true;}has[p]=false;}}
    int query(int p,int l,int r,int a,int b){if(a<=l&&r<=b)return tree[p];push(p);int m=(l+r)/2,v=0;if(a<=m)v=Math.max(v,query(p*2,l,m,a,b));if(b>m)v=Math.max(v,query(p*2+1,m+1,r,a,b));return v;}
    void assign(int p,int l,int r,int a,int b,int v){if(a<=l&&r<=b){tree[p]=v;lazy[p]=v;has[p]=true;return;}push(p);int m=(l+r)/2;if(a<=m)assign(p*2,l,m,a,b,v);if(b>m)assign(p*2+1,m+1,r,a,b,v);tree[p]=Math.max(tree[p*2],tree[p*2+1]);}
    public List<Integer> fallingSquares(int[][] positions){TreeSet<Integer> set=new TreeSet<>();for(int[]x:positions){set.add(x[0]);set.add(x[0]+x[1]);}List<Integer> c=new ArrayList<>(set);int n=c.size()-1;tree=new int[4*n+4];lazy=new int[4*n+4];has=new boolean[4*n+4];List<Integer> out=new ArrayList<>();int best=0;for(int[]x:positions){int a=Collections.binarySearch(c,x[0]),b=Collections.binarySearch(c,x[0]+x[1])-1;int h=query(1,0,n-1,a,b)+x[1];assign(1,0,n-1,a,b,h);best=Math.max(best,h);out.add(best);}return out;}
}
