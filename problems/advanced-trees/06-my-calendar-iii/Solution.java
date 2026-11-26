class MyCalendarThree {
    private final TreeMap<Integer,Integer> delta=new TreeMap<>();
    public MyCalendarThree() {}
    public int book(int start,int end) {
        delta.merge(start,1,Integer::sum);delta.merge(end,-1,Integer::sum);
        int active=0,best=0;for(int x:delta.values()){active+=x;best=Math.max(best,active);}return best;
    }
}
