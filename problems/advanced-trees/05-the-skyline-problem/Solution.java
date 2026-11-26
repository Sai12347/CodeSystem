class Solution {
    public List<List<Integer>> getSkyline(int[][] buildings) {
        int n=buildings.length;int[][] e=new int[2*n][2];int k=0;
        for(int[] b:buildings){e[k++]=new int[]{b[0],-b[2]};e[k++]=new int[]{b[1],b[2]};}
        Arrays.sort(e,(a,b)->Integer.compare(a[0],b[0]));TreeMap<Integer,Integer> active=new TreeMap<>();active.put(0,1);
        List<List<Integer>> out=new ArrayList<>();int prev=0,i=0;
        while(i<e.length){int x=e[i][0];while(i<e.length&&e[i][0]==x){int h=e[i++][1];if(h<0)active.merge(-h,1,Integer::sum);else{int c=active.get(h)-1;if(c==0)active.remove(h);else active.put(h,c);}}
            int cur=active.lastKey();if(cur!=prev){out.add(Arrays.asList(x,cur));prev=cur;}
        }return out;
    }
}
