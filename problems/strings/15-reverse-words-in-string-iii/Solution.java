class Solution { public String reverseWords(String s) { String[] w=s.split(" ",-1);for(int i=0;i<w.length;i++)w[i]=new StringBuilder(w[i]).reverse().toString();return String.join(" ",w);} }
