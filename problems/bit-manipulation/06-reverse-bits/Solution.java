class Solution { public long reverseBits(long n) { long r=0;for(int i=0;i<32;i++){r=(r<<1)|(n&1L);n>>>=1;}return r;} }
