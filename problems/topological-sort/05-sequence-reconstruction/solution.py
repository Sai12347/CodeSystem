class Solution:
    def sequenceReconstruction(self, nums: List[int], sequences: List[List[int]]) -> bool:
        n=len(nums);g=[set() for _ in range(n+1)];d=[0]*(n+1);seen=set()
        for seq in sequences:
            for x in seq:seen.add(x)
            for a,b in zip(seq,seq[1:]):
                if b not in g[a]:g[a].add(b);d[b]+=1
        if seen!=set(range(1,n+1)):return False
        q=deque(i for i in range(1,n+1) if d[i]==0);i=0
        while q:
            if len(q)!=1:return False
            u=q.popleft()
            if i>=n or nums[i]!=u:return False
            i+=1
            for v in g[u]:
                d[v]-=1
                if d[v]==0:q.append(v)
        return i==n
