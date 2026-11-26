class Solution { public int singleNumber(int[] a) { int ones=0,twos=0; for(int x:a){ones=(ones^x)&~twos;twos=(twos^x)&~ones;} return ones; } }
