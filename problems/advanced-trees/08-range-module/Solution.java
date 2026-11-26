class RangeModule {
    private final TreeMap<Integer,Integer> ranges=new TreeMap<>();
    public RangeModule() {}
    public void addRange(int left,int right) {
        Map.Entry<Integer,Integer> e=ranges.floorEntry(left);
        if(e!=null&&e.getValue()>=left){left=e.getKey();right=Math.max(right,e.getValue());ranges.remove(e.getKey());}
        e=ranges.ceilingEntry(left);while(e!=null&&e.getKey()<=right){right=Math.max(right,e.getValue());ranges.remove(e.getKey());e=ranges.ceilingEntry(left);}
        ranges.put(left,right);
    }
    public boolean queryRange(int left,int right) { Map.Entry<Integer,Integer> e=ranges.floorEntry(left);return e!=null&&e.getValue()>=right; }
    public void removeRange(int left,int right) {
        List<int[]> keep=new ArrayList<>();for(Map.Entry<Integer,Integer> e:new ArrayList<>(ranges.entrySet())){int a=e.getKey(),b=e.getValue();if(b<=left||a>=right)continue;ranges.remove(a);if(a<left)keep.add(new int[]{a,left});if(b>right)keep.add(new int[]{right,b});}
        for(int[] x:keep)ranges.put(x[0],x[1]);
    }
}
